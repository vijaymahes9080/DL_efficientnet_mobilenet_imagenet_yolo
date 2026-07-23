import React, { useState } from 'react';
import { UploadCloud, Image as ImageIcon, Sparkles, Smile, Frown, Flame, Zap } from 'lucide-react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

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

const ImagePredictorTab = ({ onInferenceComplete }) => {
  const [selectedImageB64, setSelectedImageB64] = useState(null);
  const [selectedModel, setSelectedModel] = useState('all');
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState(null);

  const handleFileUpload = (file) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      setSelectedImageB64(e.target.result);
      setResults(null);
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const loadPreset = (emotionPreset) => {
    const canvas = document.createElement('canvas');
    canvas.width = 300;
    canvas.height = 300;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, 300, 300);

    ctx.beginPath();
    ctx.arc(150, 150, 90, 0, Math.PI * 2);
    ctx.fillStyle = '#fde047';
    ctx.fill();

    ctx.fillStyle = '#000000';
    ctx.beginPath();
    ctx.arc(115, 130, 10, 0, Math.PI * 2);
    ctx.arc(185, 130, 10, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#000000';

    if (emotionPreset === 'happy') {
      ctx.arc(150, 160, 50, 0.1 * Math.PI, 0.9 * Math.PI, false);
    } else if (emotionPreset === 'angry') {
      ctx.arc(150, 200, 40, 1.1 * Math.PI, 1.9 * Math.PI, false);
      ctx.lineWidth = 5;
      ctx.moveTo(100, 110); ctx.lineTo(130, 125);
      ctx.moveTo(200, 110); ctx.lineTo(170, 125);
      ctx.stroke();
    } else if (emotionPreset === 'surprise') {
      ctx.arc(150, 180, 20, 0, Math.PI * 2);
      ctx.fill();
    } else if (emotionPreset === 'sad') {
      ctx.arc(150, 200, 45, 1.1 * Math.PI, 1.9 * Math.PI, false);
    }
    ctx.stroke();

    const dataUrl = canvas.toDataURL('image/jpeg');
    setSelectedImageB64(dataUrl);
    setResults(null);
  };

  const runInference = async () => {
    if (!selectedImageB64) return;
    setIsProcessing(true);

    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: selectedImageB64, model: selectedModel })
      });
      const data = await res.json();

      if (data.status === 'success') {
        setResults(data);
        if (onInferenceComplete) {
          onInferenceComplete(data, selectedImageB64);
        }
      }
    } catch (err) {
      alert('Prediction failed: ' + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const chartData = results ? {
    labels: CLASS_NAMES,
    datasets: [{
      label: 'Probability (%)',
      data: CLASS_NAMES.map(name => results.consensus.probabilities[name] || 0),
      backgroundColor: CLASS_NAMES.map(name => EMOTION_COLORS[name]),
      borderRadius: 6
    }]
  } : null;

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
      y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, max: 100 }
    }
  };

  return (
    <div className="grid-predictor">
      <div className="panel-box upload-section">
        <div className="panel-header">
          <h3>
            <ImageIcon size={18} /> Select or Upload Media
          </h3>
        </div>

        <div
          className="dropzone"
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          onClick={() => document.getElementById('react-file-input').click()}
        >
          <UploadCloud className="drop-icon" size={36} />
          <h4>Drag & Drop Image Here</h4>
          <p>Supports PNG, JPG, JPEG, WEBP</p>
          <input
            type="file"
            id="react-file-input"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={(e) => e.target.files && handleFileUpload(e.target.files[0])}
          />
        </div>

        <div className="sample-presets">
          <span>Test Presets:</span>
          <div className="preset-btn-group">
            <button className="preset-btn" onClick={() => loadPreset('happy')}>
              <Smile size={14} /> Happy
            </button>
            <button className="preset-btn" onClick={() => loadPreset('angry')}>
              <Flame size={14} /> Angry
            </button>
            <button className="preset-btn" onClick={() => loadPreset('surprise')}>
              <Zap size={14} /> Surprise
            </button>
            <button className="preset-btn" onClick={() => loadPreset('sad')}>
              <Frown size={14} /> Sad
            </button>
          </div>
        </div>

        <div className="predictor-options">
          <label>Inference Mode:</label>
          <select
            className="cyber-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            <option value="all">All 4 Models (Ensemble Consensus)</option>
            <option value="efficientnet">EfficientNet-B0 Only</option>
            <option value="yolov8">YOLOv8 Only</option>
            <option value="resnet">ResNet50 Only</option>
            <option value="mobilenet">MobileNetV2 Only</option>
          </select>
          <button
            className="cyber-btn primary full-width"
            onClick={runInference}
            disabled={!selectedImageB64 || isProcessing}
          >
            <Sparkles size={16} />
            {isProcessing ? 'Processing Neural Layers...' : 'Run Neural Inference'}
          </button>
        </div>
      </div>

      <div className="panel-box results-section">
        <div className="panel-header">
          <h3>Neural Diagnostics</h3>
          {results && (
            <span className="time-badge" style={{ background: 'rgba(0,242,254,0.1)', color: '#00f2fe', padding: '4px 10px', borderRadius: '4px', fontSize: '11px', fontWeight: 700 }}>
              {results.total_latency_ms} ms
            </span>
          )}
        </div>

        <div className="preview-stage">
          {selectedImageB64 ? (
            <img src={selectedImageB64} alt="Selected Preview" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          ) : (
            <div className="preview-placeholder">
              <ImageIcon size={32} />
              <p>Upload an image to render predictions</p>
            </div>
          )}
        </div>

        {results && (
          <div className="results-container">
            <div className="consensus-banner">
              <div className="consensus-title">CONSENSUS PREDICTION</div>
              <div className="consensus-body">
                <h2 style={{ color: EMOTION_COLORS[results.consensus.emotion] || '#00f2fe' }}>
                  {results.consensus.emotion.toUpperCase()}
                </h2>
                <div className="conf-pill" style={{ backgroundColor: EMOTION_COLORS[results.consensus.emotion] || '#00f2fe' }}>
                  {results.consensus.confidence}% Confidence
                </div>
              </div>
            </div>

            <div style={{ height: '180px', position: 'relative' }}>
              <Bar data={chartData} options={chartOptions} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImagePredictorTab;
