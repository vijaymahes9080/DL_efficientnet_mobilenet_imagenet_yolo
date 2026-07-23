import React from 'react';
import { Brain, Video, Upload, Layers, Eye, BarChart3, Activity } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'hud', label: 'Live HUD', icon: Video },
    { id: 'predictor', label: 'Image Predictor', icon: Upload },
    { id: 'arena', label: '4-Model Arena', icon: Layers },
    { id: 'xai', label: 'Grad-CAM XAI', icon: Eye },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  ];

  return (
    <header className="app-header">
      <div className="brand-logo">
        <Brain className="glow-icon" />
        <div className="brand-text">
          <h1>NEURAL SYNERGY</h1>
          <span className="brand-sub">FACIAL EMOTION INTELLIGENCE ECOSYSTEM</span>
        </div>
      </div>

      <nav className="nav-tabs">
        {tabs.map((tab) => {
          const IconComponent = tab.icon;
          return (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <IconComponent size={16} />
              {tab.label}
            </button>
          );
        })}
      </nav>

      <div className="system-badge">
        <span className="status-dot"></span>
        <span className="status-text">4 MODELS ONLINE</span>
      </div>
    </header>
  );
};

export default Navbar;
