import React, { useState } from 'react';
import Navbar from './components/Navbar';
import HeroModelCards from './components/HeroModelCards';
import LiveHudTab from './components/LiveHudTab';
import ImagePredictorTab from './components/ImagePredictorTab';
import ArenaTab from './components/ArenaTab';
import XaiTab from './components/XaiTab';
import AnalyticsTab from './components/AnalyticsTab';

function App() {
  const [activeTab, setActiveTab] = useState('hud');
  const [lastPrediction, setLastPrediction] = useState(null);
  const [lastBaseImage, setLastBaseImage] = useState(null);

  const handleInferenceComplete = (results, imageB64) => {
    setLastPrediction(results);
    setLastBaseImage(imageB64);
  };

  return (
    <div className="app-container">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <HeroModelCards />

      <main className="dashboard-main">
        {activeTab === 'hud' && <LiveHudTab />}
        {activeTab === 'predictor' && (
          <ImagePredictorTab onInferenceComplete={handleInferenceComplete} />
        )}
        {activeTab === 'arena' && (
          <ArenaTab predictionResults={lastPrediction} />
        )}
        {activeTab === 'xai' && (
          <XaiTab predictionResults={lastPrediction} baseImageB64={lastBaseImage} />
        )}
        {activeTab === 'analytics' && <AnalyticsTab />}
      </main>
    </div>
  );
}

export default App;
