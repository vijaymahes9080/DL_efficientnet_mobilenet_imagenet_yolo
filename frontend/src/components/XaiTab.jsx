import React, { useState } from 'react';
import { Sliders, Eye } from 'lucide-react';

const XaiTab = ({ predictionResults, baseImageB64 }) => {
  const [opacity, setOpacity] = useState(70);

  const gradCamOverlay = predictionResults?.grad_cam_overlay;

  return (
    <div className="xai-container">
      <div className="xai-sidebar panel-box">
        <div className="panel-header">
          <h3>
            <Sliders size={18} /> Saliency Controls
          </h3>
        </div>

        <div className="xai-control-group">
          <label>Heatmap Opacity: {opacity}%</label>
          <input
            type="range"
            min="0"
            max="100"
            value={opacity}
            className="cyber-range"
            onChange={(e) => setOpacity(Number(e.target.value))}
          />
        </div>

        <div className="xai-info-card">
          <h4>Grad-CAM Insights</h4>
          <p>
            Visualizes regions of interest driving emotion decisions. Bright red/yellow areas indicate high facial muscle gradient influence (mouth contour, eye squinting, brow furrows).
          </p>
        </div>
      </div>

      <div className="stage-card">
        <h4>Grad-CAM Heatmap Overlay</h4>
        <div className="xai-image-wrap">
          {baseImageB64 && <img src={baseImageB64} alt="Base Image" />}
          {gradCamOverlay ? (
            <img
              src={gradCamOverlay}
              alt="Heatmap Overlay"
              style={{ opacity: opacity / 100 }}
            />
          ) : (
            <div className="xai-placeholder">
              <Eye size={40} />
              <p>Run prediction in Image Predictor to load Grad-CAM heatmap</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default XaiTab;
