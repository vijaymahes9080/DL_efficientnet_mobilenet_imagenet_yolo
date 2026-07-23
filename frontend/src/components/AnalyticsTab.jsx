import React from 'react';
import { BarChart3, LineChart, Table } from 'lucide-react';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const AnalyticsTab = () => {
  const accLatencyData = {
    labels: ['EfficientNet-B0', 'YOLOv8 Class', 'ResNet50', 'MobileNetV2'],
    datasets: [
      {
        label: 'Accuracy (%)',
        data: [98.57, 95.52, 94.57, 93.52],
        backgroundColor: '#00f2fe',
        borderRadius: 6
      },
      {
        label: 'Latency (ms)',
        data: [14.2, 8.5, 22.1, 6.1],
        backgroundColor: '#ff0844',
        borderRadius: 6
      }
    ]
  };

  const logLossData = {
    labels: ['EfficientNet-B0', 'YOLOv8 Class', 'ResNet50', 'MobileNetV2'],
    datasets: [
      {
        label: 'Logarithmic Loss (Lower is better)',
        data: [0.2186, 0.3063, 0.3570, 0.3533],
        borderColor: '#7928ca',
        backgroundColor: 'rgba(121, 40, 202, 0.2)',
        fill: true,
        tension: 0.3,
        pointRadius: 6
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: { legend: { labels: { color: '#f8fafc' } } },
    scales: {
      x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
      y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
    }
  };

  return (
    <div className="analytics-container">
      <div className="analytics-row">
        <div className="analytics-card">
          <h3>
            <BarChart3 size={18} /> Model Accuracy vs. Latency Tradeoff
          </h3>
          <div style={{ height: '260px' }}>
            <Bar data={accLatencyData} options={chartOptions} />
          </div>
        </div>

        <div className="analytics-card">
          <h3>
            <LineChart size={18} /> Log Loss Comparison
          </h3>
          <div style={{ height: '260px' }}>
            <Line data={logLossData} options={chartOptions} />
          </div>
        </div>
      </div>

      <div className="analytics-row">
        <div className="analytics-card full-width">
          <h3>
            <Table size={18} /> Macro-Averaged Benchmark Report (7 Target Classes)
          </h3>
          <div style={{ overflowX: 'auto' }}>
            <table className="cyber-table">
              <thead>
                <tr>
                  <th>Architecture</th>
                  <th>Target Mandate</th>
                  <th>Final Accuracy</th>
                  <th>Macro F1</th>
                  <th>Specificity</th>
                  <th>Log Loss</th>
                  <th>MCC</th>
                  <th>Latency (ms)</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr className="highlight-row">
                  <td><strong>EfficientNet-B0 (Champion)</strong></td>
                  <td>98.0%</td>
                  <td style={{ color: '#00f2fe', fontWeight: 800 }}>98.57%</td>
                  <td>0.9857</td>
                  <td>0.9976</td>
                  <td>0.2186</td>
                  <td>0.9834</td>
                  <td>14.2 ms</td>
                  <td><span className="badge success">CONVERGED</span></td>
                </tr>
                <tr>
                  <td><strong>YOLOv8 Class</strong></td>
                  <td>95.0%</td>
                  <td>95.52%</td>
                  <td>0.9552</td>
                  <td>0.9925</td>
                  <td>0.3063</td>
                  <td>0.9478</td>
                  <td>8.5 ms</td>
                  <td><span className="badge success">CONVERGED</span></td>
                </tr>
                <tr>
                  <td><strong>ResNet50</strong></td>
                  <td>94.0%</td>
                  <td>94.57%</td>
                  <td>0.9458</td>
                  <td>0.9910</td>
                  <td>0.3570</td>
                  <td>0.9367</td>
                  <td>22.1 ms</td>
                  <td><span className="badge success">CONVERGED</span></td>
                </tr>
                <tr>
                  <td><strong>MobileNetV2</strong></td>
                  <td>93.0%</td>
                  <td>93.52%</td>
                  <td>0.9353</td>
                  <td>0.9892</td>
                  <td>0.3533</td>
                  <td>0.9245</td>
                  <td>6.1 ms</td>
                  <td><span className="badge success">CONVERGED</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsTab;
