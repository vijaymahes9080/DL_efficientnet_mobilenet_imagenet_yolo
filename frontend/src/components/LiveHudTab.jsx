import React, { useState, useRef, useEffect } from 'react';
import { Camera, Power, Activity, BarChart2 } from 'lucide-react';

const CLASS_NAMES = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise'];
const EMOTION_COLORS = {
  'Angry': '#ef4444',
  'Disgust': '#10b981',
  'Fear': '#a855f7',
  'Happy': '#eab308',
  'Neutral': '#94a3b8',
  'Sad': '#3b82f6',
  'Surprise': '#f97316'
};

const LiveHudTab = () => {
  const [isCameraRunning, setIsCameraRunning] = useState(false);
  const [selectedModel, setSelectedModel] = useState('efficientnet');
  const [fps, setFps] = useState(0);
  const [latency, setLatency] = useState(0);
  const [dominantEmotion, setDominantEmotion] = useState('AWAITING FEED');
  const [confidence, setConfidence] = useState(0);
  const [probabilities, setProbabilities] = useState({
    Angry: 0, Disgust: 0, Fear: 0, Happy: 0, Neutral: 0, Sad: 0, Surprise: 0
  });

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);
  const lastFrameTimeRef = useRef(Date.now());

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' }
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setIsCameraRunning(true);
      intervalRef.current = setInterval(processFrame, 120);
    } catch (err) {
      alert('Camera access error: ' + err.message);
    }
  };

  const stopCamera = () => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }
    setIsCameraRunning(false);
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
    setDominantEmotion('AWAITING FEED');
    setConfidence(0);
  };

  const processFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const now = Date.now();
    const currentFps = Math.round(1000 / (now - lastFrameTimeRef.current));
    lastFrameTimeRef.current = now;
    setFps(currentFps);

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);

    const frameB64 = tempCanvas.toDataURL('image/jpeg', 0.8);

    try {
      const res = await fetch('/api/predict_frame', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ frame: frameB64, model: selectedModel })
      });
      const data = await res.json();

      if (data.status === 'success') {
        setLatency(data.latency_ms);
        drawBoundingBox(data);
      }
    } catch (err) {
      console.error('Frame prediction error:', err);
    }
  };

  const drawBoundingBox = (data) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (data.face_detected && data.bounding_box) {
      const [x, y, w, h] = data.bounding_box;
      const emotion = data.dominant_emotion;
      const conf = data.confidence;
      const color = EMOTION_COLORS[emotion] || '#00f2fe';

      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.strokeRect(x, y, w, h);

      ctx.fillStyle = color;
      ctx.fillRect(x, y - 28, Math.max(140, w), 28);

      ctx.fillStyle = '#000000';
      ctx.font = 'bold 14px Outfit, sans-serif';
      ctx.fillText(`${emotion.toUpperCase()} (${conf}%)`, x + 8, y - 9);

      setDominantEmotion(emotion.toUpperCase());
      setConfidence(conf);
      setProbabilities(data.probabilities || {});
    }
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="grid-hud">
      <div className="viewport-box">
        <div className="viewport-header">
          <span className="view-title">
            <Camera size={18} /> REAL-TIME CAMERA FEED
          </span>
          <div className="hud-controls">
            <label htmlFor="hud-model-select">Active Model:</label>
            <select
              id="hud-model-select"
              className="cyber-select"
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
            >
              <option value="efficientnet">EfficientNet-B0 (98.57%)</option>
              <option value="yolov8">YOLOv8 (95.52%)</option>
              <option value="resnet">ResNet50 (94.57%)</option>
              <option value="mobilenet">MobileNetV2 (93.52%)</option>
            </select>
            <button
              className={`cyber-btn ${isCameraRunning ? 'secondary' : 'primary'}`}
              onClick={isCameraRunning ? stopCamera : startCamera}
            >
              <Power size={14} />
              {isCameraRunning ? 'Stop Camera' : 'Start Camera'}
            </button>
          </div>
        </div>

        <div className="video-container">
          <video ref={videoRef} autoPlay playsInline muted style={{ display: isCameraRunning ? 'block' : 'none' }}></video>
          <canvas ref={canvasRef} style={{ display: isCameraRunning ? 'block' : 'none' }}></canvas>

          {!isCameraRunning && (
            <div className="cam-placeholder">
              <Camera className="cam-icon" size={48} />
              <p>Click "Start Camera" to initialize 10X Real-Time HUD</p>
            </div>
          )}

          {isCameraRunning && (
            <div className="hud-overlay-info">
              <span>FPS: {fps}</span>
              <span>Latency: {latency} ms</span>
            </div>
          )}
        </div>
      </div>

      <div className="sidebar-box">
        <div className="panel-header">
          <h3>
            <BarChart2 size={18} /> Emotion Probabilities
          </h3>
          <span className="live-tag">LIVE</span>
        </div>

        <div className="dominant-emotion-display">
          <div className="dom-label" style={{ color: EMOTION_COLORS[dominantEmotion] || '#00f2fe' }}>
            {dominantEmotion}
          </div>
          <div className="dom-conf">{confidence}% Confidence</div>
        </div>

        <div className="bars-container">
          {CLASS_NAMES.map((name) => {
            const val = probabilities[name] || 0;
            return (
              <div key={name} className="prob-row">
                <div className="prob-meta">
                  <span style={{ color: EMOTION_COLORS[name] }}>{name}</span>
                  <span>{val}%</span>
                </div>
                <div className="prob-track">
                  <div
                    className="prob-fill"
                    style={{
                      width: `${val}%`,
                      backgroundColor: EMOTION_COLORS[name]
                    }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default LiveHudTab;
