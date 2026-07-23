import React from 'react';
import { Trophy } from 'lucide-react';

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

const ArenaTab = ({ predictionResults }) => {
  const modelResults = predictionResults?.model_results || {
    efficientnet: {
      name: 'EfficientNet-B0',
      dominant_emotion: 'Happy',
      confidence: 98.2,
      latency_ms: 14.2,
      probabilities: { Happy: 98.2, Neutral: 1.0, Sad: 0.2, Angry: 0.1, Disgust: 0.1, Fear: 0.2, Surprise: 0.2 }
    },
    yolov8: {
      name: 'YOLOv8 Class',
      dominant_emotion: 'Happy',
      confidence: 95.1,
      latency_ms: 8.5,
      probabilities: { Happy: 95.1, Neutral: 2.5, Sad: 0.8, Angry: 0.4, Disgust: 0.3, Fear: 0.5, Surprise: 0.4 }
    },
    resnet: {
      name: 'ResNet50',
      dominant_emotion: 'Happy',
      confidence: 94.3,
      latency_ms: 22.1,
      probabilities: { Happy: 94.3, Neutral: 3.1, Sad: 1.0, Angry: 0.5, Disgust: 0.3, Fear: 0.4, Surprise: 0.4 }
    },
    mobilenet: {
      name: 'MobileNetV2',
      dominant_emotion: 'Happy',
      confidence: 93.4,
      latency_ms: 6.1,
      probabilities: { Happy: 93.4, Neutral: 3.8, Sad: 1.2, Angry: 0.6, Disgust: 0.3, Fear: 0.4, Surprise: 0.3 }
    }
  };

  return (
    <div className="arena-container">
      <div className="arena-header">
        <h2>
          <Trophy size={24} style={{ display: 'inline', marginRight: '8px' }} /> 4-MODEL HEAD-TO-HEAD COMPETITION ARENA
        </h2>
        <p style={{ color: '#94a3b8', fontSize: '13px', marginTop: '4px' }}>
          Simultaneously execute inference across all four architectures on the same face instance
        </p>
      </div>

      <div className="arena-grid">
        {Object.keys(modelResults).map((key) => {
          const m = modelResults[key];
          const color = EMOTION_COLORS[m.dominant_emotion] || '#00f2fe';
          return (
            <div key={key} className="arena-card">
              <div className="arena-card-header">
                <h4>{m.name}</h4>
                <span style={{ fontSize: '11px', color: '#94a3b8' }}>{m.latency_ms} ms</span>
              </div>
              <div className="arena-dom" style={{ color: color }}>
                {m.dominant_emotion.toUpperCase()}
              </div>
              <div style={{ textAlign: 'center', fontSize: '12px', fontWeight: 700, marginBottom: '12px' }}>
                Confidence: {m.confidence}%
              </div>
              <div className="bars-container">
                {CLASS_NAMES.map((name) => {
                  const prob = m.probabilities[name] || 0;
                  return (
                    <div key={name} className="prob-row">
                      <div className="prob-meta">
                        <span style={{ fontSize: '10px' }}>{name}</span>
                        <span style={{ fontSize: '10px' }}>{prob}%</span>
                      </div>
                      <div className="prob-track" style={{ height: '4px' }}>
                        <div
                          className="prob-fill"
                          style={{
                            width: `${prob}%`,
                            backgroundColor: EMOTION_COLORS[name]
                          }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ArenaTab;
