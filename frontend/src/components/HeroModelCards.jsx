import React from 'react';

const HeroModelCards = () => {
  const models = [
    {
      id: 'efficientnet',
      name: 'EfficientNet-B0',
      acc: '98.57%',
      role: 'CHAMPION',
      isChampion: true,
      logLoss: '0.2186',
      mcc: '0.9834',
      latency: '14.2 ms'
    },
    {
      id: 'yolov8',
      name: 'YOLOv8 Class',
      acc: '95.52%',
      role: 'STREAMING',
      isRunnerup: true,
      logLoss: '0.3063',
      mcc: '0.9478',
      latency: '8.5 ms'
    },
    {
      id: 'resnet',
      name: 'ResNet50',
      acc: '94.57%',
      logLoss: '0.3570',
      mcc: '0.9367',
      latency: '22.1 ms'
    },
    {
      id: 'mobilenet',
      name: 'MobileNetV2',
      acc: '93.52%',
      logLoss: '0.3533',
      mcc: '0.9245',
      latency: '6.1 ms'
    }
  ];

  return (
    <section className="hero-models-bar">
      {models.map((m) => (
        <div
          key={m.id}
          className={`model-card ${m.isChampion ? 'champion' : ''} ${m.isRunnerup ? 'runnerup' : ''}`}
        >
          {m.role && <div className="card-badge">{m.role}</div>}
          <div className="card-header">
            <h3>{m.name}</h3>
            <span className="model-acc">{m.acc}</span>
          </div>
          <div className="card-body">
            <div className="card-stat">
              <span>Log Loss:</span>
              <strong>{m.logLoss}</strong>
            </div>
            <div className="card-stat">
              <span>MCC:</span>
              <strong>{m.mcc}</strong>
            </div>
            <div className="card-stat">
              <span>Latency:</span>
              <strong>{m.latency}</strong>
            </div>
          </div>
          <div className="card-glow-bar"></div>
        </div>
      ))}
    </section>
  );
};

export default HeroModelCards;
