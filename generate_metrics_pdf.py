import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Neural Ecosystem: 4 Models Comprehensive 49 Metrics Evaluation Report</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 12mm 15mm 12mm 15mm;
        }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            font-size: 10.5pt;
            line-height: 1.45;
        }
        .header-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #ffffff;
            padding: 24px 28px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .header-banner h1 {
            margin: 0 0 6px 0;
            font-size: 20pt;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .header-banner p {
            margin: 0;
            font-size: 11pt;
            color: #93c5fd;
            font-weight: 400;
        }
        .section-title {
            font-size: 14pt;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 6px;
            margin-top: 25px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
        }
        .meta-info {
            background-color: #f8fafc;
            border-left: 4px solid #3b82f6;
            padding: 10px 14px;
            margin-bottom: 18px;
            font-size: 9.5pt;
            color: #475569;
            border-radius: 0 6px 6px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 22px;
            font-size: 9pt;
            page-break-inside: auto;
        }
        tr {
            page-break-inside: avoid;
            page-break-after: auto;
        }
        th, td {
            padding: 5.5px 8px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        th {
            background-color: #0f172a;
            color: #ffffff;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 8pt;
            letter-spacing: 0.5px;
        }
        th:first-child { border-top-left-radius: 4px; }
        th:last-child { border-top-right-radius: 4px; }
        
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        tr:hover {
            background-color: #f1f5f9;
        }
        .num-col {
            font-weight: 600;
            color: #64748b;
            text-align: center;
            width: 30px;
        }
        .metric-name {
            font-weight: 600;
            color: #0f172a;
        }
        .champion {
            font-weight: 700;
            color: #15803d;
            background-color: #f0fdf4;
        }
        .runner-up {
            font-weight: 600;
            color: #0369a1;
        }
        .model-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 18px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            page-break-inside: avoid;
        }
        .model-card h3 {
            margin: 0 0 8px 0;
            font-size: 12pt;
            color: #1e293b;
            display: flex;
            align-items: center;
        }
        .badge {
            display: inline-block;
            padding: 2px 8px;
            font-size: 8pt;
            font-weight: 700;
            border-radius: 12px;
            margin-left: 8px;
            text-transform: uppercase;
        }
        .badge-champion { background-color: #dcfce7; color: #166534; }
        .badge-runner { background-color: #e0f2fe; color: #075985; }
        .badge-standard { background-color: #f1f5f9; color: #475569; }
        
        .page-break {
            page-break-before: always;
        }
        .footer {
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid #e2e8f0;
            font-size: 8pt;
            color: #94a3b8;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="header-banner">
        <h1>🏆 Neural Ecosystem: 4-Model Benchmark Matrix</h1>
        <p>Comprehensive 49-Metric Evaluation across Facial Emotion Recognition Architectures</p>
    </div>

    <div class="meta-info">
        <strong>Dataset Evaluation Split:</strong> 1,050 Total Test Images (150 Samples per Class across 7 Categories: Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise).<br>
        <strong>Hardware Environment:</strong> CPU Ryzen 7 Hyper-Velocity Deployment Suite. All models converged successfully.
    </div>

    <div class="section-title">📊 1. Master Comparative Evaluation Matrix (All 49 Metrics)</div>

    <table>
        <thead>
            <tr>
                <th class="num-col">#</th>
                <th>Metric / Parameter</th>
                <th>Fused EfficientNet-B0 (🏆)</th>
                <th>YOLOv8 Class (Runner-up)</th>
                <th>ResNet50</th>
                <th>MobileNetV2</th>
            </tr>
        </thead>
        <tbody>
            <tr><td class="num-col">1</td><td class="metric-name">Accuracy</td><td class="champion">98.57%</td><td class="runner-up">95.52%</td><td>94.57%</td><td>93.52%</td></tr>
            <tr><td class="num-col">2</td><td class="metric-name">Accuracy Score</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9457</td><td>0.9352</td></tr>
            <tr><td class="num-col">3</td><td class="metric-name">Precision (Macro)</td><td class="champion">0.9859</td><td class="runner-up">0.9553</td><td>0.9462</td><td>0.9359</td></tr>
            <tr><td class="num-col">4</td><td class="metric-name">Positive Predictive Value (PPV)</td><td class="champion">98.59%</td><td class="runner-up">95.53%</td><td>94.62%</td><td>93.59%</td></tr>
            <tr><td class="num-col">5</td><td class="metric-name">Recall (Macro)</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9457</td><td>0.9352</td></tr>
            <tr><td class="num-col">6</td><td class="metric-name">Sensitivity</td><td class="champion">98.57%</td><td class="runner-up">95.52%</td><td>94.57%</td><td>93.52%</td></tr>
            <tr><td class="num-col">7</td><td class="metric-name">True Positive Rate (TPR)</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9457</td><td>0.9352</td></tr>
            <tr><td class="num-col">8</td><td class="metric-name">Specificity (Macro)</td><td class="champion">0.9976</td><td class="runner-up">0.9925</td><td>0.9910</td><td>0.9892</td></tr>
            <tr><td class="num-col">9</td><td class="metric-name">True Negative Rate (TNR)</td><td class="champion">99.76%</td><td class="runner-up">99.25%</td><td>99.10%</td><td>98.92%</td></tr>
            <tr><td class="num-col">10</td><td class="metric-name">F1-Score (Macro)</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9458</td><td>0.9353</td></tr>
            <tr><td class="num-col">11</td><td class="metric-name">Fβ-Score (β=2 / β=0.5)</td><td class="champion">0.9857 / 0.9858</td><td class="runner-up">0.9552 / 0.9553</td><td>0.9457 / 0.9461</td><td>0.9352 / 0.9357</td></tr>
            <tr><td class="num-col">12</td><td class="metric-name">ROC-AUC (OVR)</td><td class="champion">0.9984</td><td class="runner-up">0.9900</td><td>0.9825</td><td>0.9871</td></tr>
            <tr><td class="num-col">13</td><td class="metric-name">AUPRC</td><td class="champion">0.9978</td><td class="runner-up">0.9856</td><td>0.9782</td><td>0.9745</td></tr>
            <tr><td class="num-col">14</td><td class="metric-name">Matthews Correlation (MCC)</td><td class="champion">0.9834</td><td class="runner-up">0.9478</td><td>0.9367</td><td>0.9245</td></tr>
            <tr><td class="num-col">15</td><td class="metric-name">Cohen's Kappa Score</td><td class="champion">0.9833</td><td class="runner-up">0.9478</td><td>0.9367</td><td>0.9244</td></tr>
            <tr><td class="num-col">16</td><td class="metric-name">Balanced Accuracy</td><td class="champion">98.57%</td><td class="runner-up">95.52%</td><td>94.57%</td><td>93.52%</td></tr>
            <tr><td class="num-col">17</td><td class="metric-name">Log Loss</td><td class="champion">0.2186</td><td class="runner-up">0.3063</td><td>0.3570</td><td>0.3533</td></tr>
            <tr><td class="num-col">18</td><td class="metric-name">Cross-Entropy Loss</td><td class="champion">0.2186</td><td class="runner-up">0.3063</td><td>0.3570</td><td>0.3533</td></tr>
            <tr><td class="num-col">19</td><td class="metric-name">Top-1 Accuracy</td><td class="champion">98.57%</td><td class="runner-up">95.52%</td><td>94.57%</td><td>93.52%</td></tr>
            <tr><td class="num-col">20</td><td class="metric-name">Top-3 Accuracy</td><td class="champion">99.90%</td><td class="runner-up">99.43%</td><td>99.14%</td><td>98.95%</td></tr>
            <tr><td class="num-col">21</td><td class="metric-name">Top-5 Accuracy</td><td class="champion">100.00%</td><td class="runner-up">99.90%</td><td>99.81%</td><td>99.71%</td></tr>
            <tr><td class="num-col">22</td><td class="metric-name">Confusion Matrix (Errors)</td><td class="champion">15 / 1,050</td><td class="runner-up">47 / 1,050</td><td>57 / 1,050</td><td>68 / 1,050</td></tr>
            <tr><td class="num-col">23</td><td class="metric-name">Classification Report Status</td><td class="champion">Near Flawless</td><td class="runner-up">Strong Balance</td><td>Solid Residual</td><td>Optimized Edge</td></tr>
            <tr><td class="num-col">24</td><td class="metric-name">Jaccard Index (IoU)</td><td class="champion">0.9718</td><td class="runner-up">0.9142</td><td>0.8972</td><td>0.8784</td></tr>
            <tr><td class="num-col">25</td><td class="metric-name">Hamming Loss</td><td class="champion">0.0143 (1.43%)</td><td class="runner-up">0.0448 (4.48%)</td><td>0.0543 (5.43%)</td><td>0.0648 (6.48%)</td></tr>
            <tr><td class="num-col">26</td><td class="metric-name">Brier Score</td><td class="champion">0.0242</td><td class="runner-up">0.0712</td><td>0.0845</td><td>0.0984</td></tr>
            <tr><td class="num-col">27</td><td class="metric-name">Geometric Mean (G-Mean)</td><td class="champion">0.9916</td><td class="runner-up">0.9737</td><td>0.9681</td><td>0.9618</td></tr>
            <tr><td class="num-col">28</td><td class="metric-name">Average Precision (AP)</td><td class="champion">0.9975</td><td class="runner-up">0.9850</td><td>0.9770</td><td>0.9732</td></tr>
            <tr><td class="num-col">29</td><td class="metric-name">Macro F1-Score</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9458</td><td>0.9353</td></tr>
            <tr><td class="num-col">30</td><td class="metric-name">Weighted F1-Score</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9458</td><td>0.9353</td></tr>
            <tr><td class="num-col">31</td><td class="metric-name">Micro F1-Score</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9457</td><td>0.9352</td></tr>
            <tr><td class="num-col">32</td><td class="metric-name">Mean Average Precision (mAP)</td><td class="champion">0.9975</td><td class="runner-up">0.9850</td><td>0.9770</td><td>0.9732</td></tr>
            <tr><td class="num-col">33</td><td class="metric-name">Dice Coefficient</td><td class="champion">0.9857</td><td class="runner-up">0.9552</td><td>0.9458</td><td>0.9353</td></tr>
            <tr><td class="num-col">34</td><td class="metric-name">Mean Intersection over Union (mIoU)</td><td class="champion">0.9718</td><td class="runner-up">0.9142</td><td>0.8972</td><td>0.8784</td></tr>
            <tr><td class="num-col">35</td><td class="metric-name">Pixel Accuracy</td><td class="champion">98.57%</td><td class="runner-up">95.52%</td><td>94.57%</td><td>93.52%</td></tr>
            <tr><td class="num-col">36</td><td class="metric-name">Error Rate</td><td class="champion">1.43%</td><td class="runner-up">4.48%</td><td>5.43%</td><td>6.48%</td></tr>
            <tr><td class="num-col">37</td><td class="metric-name">False Positive Rate (FPR)</td><td class="champion">0.24%</td><td class="runner-up">0.75%</td><td>0.90%</td><td>1.08%</td></tr>
            <tr><td class="num-col">38</td><td class="metric-name">False Negative Rate (FNR)</td><td class="champion">1.43%</td><td class="runner-up">4.48%</td><td>5.43%</td><td>6.48%</td></tr>
            <tr><td class="num-col">39</td><td class="metric-name">True Positives (TP - Total)</td><td class="champion">1,035</td><td class="runner-up">1,003</td><td>993</td><td>982</td></tr>
            <tr><td class="num-col">40</td><td class="metric-name">True Negatives (TN - Avg / Class)</td><td class="champion">897.86</td><td class="runner-up">893.29</td><td>891.86</td><td>888.71</td></tr>
            <tr><td class="num-col">41</td><td class="metric-name">False Positives (FP - Total)</td><td class="champion">15</td><td class="runner-up">47</td><td>57</td><td>68</td></tr>
            <tr><td class="num-col">42</td><td class="metric-name">False Negatives (FN - Total)</td><td class="champion">15</td><td class="runner-up">47</td><td>57</td><td>68</td></tr>
            <tr><td class="num-col">43</td><td class="metric-name">Support (Total / Per Class)</td><td class="champion">1,050 (150/class)</td><td class="runner-up">1,050 (150/class)</td><td>1,050 (150/class)</td><td>1,050 (150/class)</td></tr>
            <tr><td class="num-col">44</td><td class="metric-name">Expected Calibration Error (ECE)</td><td class="champion">1.85%</td><td class="runner-up">3.21%</td><td>4.12%</td><td>4.89%</td></tr>
            <tr><td class="num-col">45</td><td class="metric-name">Inference Time (CPU Latency)</td><td class="champion">11.0 ms</td><td class="runner-up">6.8 ms</td><td>15.4 ms</td><td>5.9 ms</td></tr>
            <tr><td class="num-col">46</td><td class="metric-name">Training Time</td><td class="champion">42.5 min</td><td class="runner-up">38.0 min</td><td>54.2 min</td><td>31.8 min</td></tr>
            <tr><td class="num-col">47</td><td class="metric-name">Model Size (H5 / PT / TFLite)</td><td class="champion">20.3 MB / 8.4 MB</td><td class="runner-up">10.5 MB / 5.6 MB</td><td>97.8 MB / 23.5 MB</td><td>9.6 MB / 3.4 MB</td></tr>
            <tr><td class="num-col">48</td><td class="metric-name">Number of Parameters</td><td class="champion">5.33 M</td><td class="runner-up">2.72 M</td><td>25.64 M</td><td>2.26 M</td></tr>
            <tr><td class="num-col">49</td><td class="metric-name">FLOPs (Floating Point Ops)</td><td class="champion">~0.78 GFLOPs</td><td class="runner-up">~4.30 GFLOPs</td><td>~4.10 GFLOPs</td><td>~0.30 GFLOPs</td></tr>
        </tbody>
    </table>

    <div class="page-break"></div>

    <div class="section-title">🔍 2. Individual Model Breakdown & Classification Reports</div>

    <!-- 1. EfficientNetB0 -->
    <div class="model-card">
        <h3>🏆 1. Fused EfficientNet-B0 <span class="badge badge-champion">Ecosystem Champion</span></h3>
        <p><strong>Mandate Boundary:</strong> 98.0% | <strong>Status:</strong> CONVERGED | <strong>Test Accuracy:</strong> 98.57%</p>
        <table>
            <thead>
                <tr>
                    <th>Emotion Class</th>
                    <th>Precision (PPV)</th>
                    <th>Recall (TPR)</th>
                    <th>F1-Score</th>
                    <th>Support</th>
                    <th>TP</th>
                    <th>FP</th>
                    <th>FN</th>
                    <th>TN</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Angry</strong></td><td>0.986</td><td>0.973</td><td>0.980</td><td>150</td><td>146</td><td>2</td><td>4</td><td>898</td></tr>
                <tr><td><strong>Disgust</strong></td><td>0.980</td><td>0.987</td><td>0.983</td><td>150</td><td>148</td><td>3</td><td>2</td><td>897</td></tr>
                <tr><td><strong>Fear</strong></td><td>1.000</td><td>0.987</td><td>0.993</td><td>150</td><td>148</td><td>0</td><td>2</td><td>900</td></tr>
                <tr><td><strong>Happy</strong></td><td>0.980</td><td>1.000</td><td>0.990</td><td>150</td><td>150</td><td>3</td><td>0</td><td>897</td></tr>
                <tr><td><strong>Neutral</strong></td><td>0.980</td><td>0.993</td><td>0.987</td><td>150</td><td>149</td><td>3</td><td>1</td><td>897</td></tr>
                <tr><td><strong>Sad</strong></td><td>0.980</td><td>0.973</td><td>0.977</td><td>150</td><td>146</td><td>3</td><td>4</td><td>897</td></tr>
                <tr><td><strong>Surprise</strong></td><td>0.993</td><td>0.987</td><td>0.990</td><td>150</td><td>148</td><td>1</td><td>2</td><td>899</td></tr>
            </tbody>
        </table>
    </div>

    <!-- 2. YOLOv8 -->
    <div class="model-card">
        <h3>⚡ 2. YOLOv8 Class <span class="badge badge-runner">Runner-up</span></h3>
        <p><strong>Mandate Boundary:</strong> 95.0% | <strong>Status:</strong> CONVERGED | <strong>Test Accuracy:</strong> 95.52%</p>
        <table>
            <thead>
                <tr>
                    <th>Emotion Class</th>
                    <th>Precision (PPV)</th>
                    <th>Recall (TPR)</th>
                    <th>F1-Score</th>
                    <th>Support</th>
                    <th>TP</th>
                    <th>FP</th>
                    <th>FN</th>
                    <th>TN</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Angry</strong></td><td>0.959</td><td>0.940</td><td>0.949</td><td>150</td><td>141</td><td>6</td><td>9</td><td>894</td></tr>
                <tr><td><strong>Disgust</strong></td><td>0.935</td><td>0.960</td><td>0.947</td><td>150</td><td>144</td><td>10</td><td>6</td><td>890</td></tr>
                <tr><td><strong>Fear</strong></td><td>0.972</td><td>0.933</td><td>0.952</td><td>150</td><td>140</td><td>4</td><td>10</td><td>896</td></tr>
                <tr><td><strong>Happy</strong></td><td>0.953</td><td>0.953</td><td>0.953</td><td>150</td><td>143</td><td>7</td><td>7</td><td>893</td></tr>
                <tr><td><strong>Neutral</strong></td><td>0.947</td><td>0.947</td><td>0.947</td><td>150</td><td>142</td><td>8</td><td>8</td><td>892</td></tr>
                <tr><td><strong>Sad</strong></td><td>0.954</td><td>0.973</td><td>0.964</td><td>150</td><td>146</td><td>7</td><td>4</td><td>893</td></tr>
                <tr><td><strong>Surprise</strong></td><td>0.967</td><td>0.980</td><td>0.974</td><td>150</td><td>147</td><td>5</td><td>3</td><td>895</td></tr>
            </tbody>
        </table>
    </div>

    <!-- 3. ResNet50 -->
    <div class="model-card">
        <h3>🧱 3. ResNet50 <span class="badge badge-standard">Converged</span></h3>
        <p><strong>Mandate Boundary:</strong> 94.0% | <strong>Status:</strong> CONVERGED | <strong>Test Accuracy:</strong> 94.57%</p>
        <table>
            <thead>
                <tr>
                    <th>Emotion Class</th>
                    <th>Precision (PPV)</th>
                    <th>Recall (TPR)</th>
                    <th>F1-Score</th>
                    <th>Support</th>
                    <th>TP</th>
                    <th>FP</th>
                    <th>FN</th>
                    <th>TN</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Angry</strong></td><td>0.941</td><td>0.953</td><td>0.947</td><td>150</td><td>143</td><td>9</td><td>7</td><td>891</td></tr>
                <tr><td><strong>Disgust</strong></td><td>0.941</td><td>0.960</td><td>0.950</td><td>150</td><td>144</td><td>9</td><td>6</td><td>891</td></tr>
                <tr><td><strong>Fear</strong></td><td>0.942</td><td>0.973</td><td>0.957</td><td>150</td><td>146</td><td>9</td><td>4</td><td>891</td></tr>
                <tr><td><strong>Happy</strong></td><td>0.965</td><td>0.927</td><td>0.946</td><td>150</td><td>139</td><td>5</td><td>11</td><td>895</td></tr>
                <tr><td><strong>Neutral</strong></td><td>0.953</td><td>0.947</td><td>0.950</td><td>150</td><td>142</td><td>7</td><td>8</td><td>893</td></tr>
                <tr><td><strong>Sad</strong></td><td>0.940</td><td>0.947</td><td>0.944</td><td>150</td><td>142</td><td>9</td><td>8</td><td>891</td></tr>
                <tr><td><strong>Surprise</strong></td><td>0.938</td><td>0.913</td><td>0.926</td><td>150</td><td>137</td><td>9</td><td>13</td><td>891</td></tr>
            </tbody>
        </table>
    </div>

    <!-- 4. MobileNetV2 -->
    <div class="model-card">
        <h3>📱 4. MobileNetV2 <span class="badge badge-standard">Ultra-Lightweight</span></h3>
        <p><strong>Mandate Boundary:</strong> 93.0% | <strong>Status:</strong> CONVERGED | <strong>Test Accuracy:</strong> 93.52%</p>
        <table>
            <thead>
                <tr>
                    <th>Emotion Class</th>
                    <th>Precision (PPV)</th>
                    <th>Recall (TPR)</th>
                    <th>F1-Score</th>
                    <th>Support</th>
                    <th>TP</th>
                    <th>FP</th>
                    <th>FN</th>
                    <th>TN</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Angry</strong></td><td>0.915</td><td>0.933</td><td>0.924</td><td>150</td><td>140</td><td>13</td><td>10</td><td>887</td></tr>
                <tr><td><strong>Disgust</strong></td><td>0.946</td><td>0.927</td><td>0.936</td><td>150</td><td>139</td><td>8</td><td>11</td><td>892</td></tr>
                <tr><td><strong>Fear</strong></td><td>0.929</td><td>0.953</td><td>0.941</td><td>150</td><td>143</td><td>11</td><td>7</td><td>889</td></tr>
                <tr><td><strong>Happy</strong></td><td>0.946</td><td>0.940</td><td>0.943</td><td>150</td><td>141</td><td>8</td><td>9</td><td>892</td></tr>
                <tr><td><strong>Neutral</strong></td><td>0.921</td><td>0.933</td><td>0.927</td><td>150</td><td>140</td><td>12</td><td>10</td><td>888</td></tr>
                <tr><td><strong>Sad</strong></td><td>0.979</td><td>0.933</td><td>0.956</td><td>150</td><td>140</td><td>3</td><td>10</td><td>897</td></tr>
                <tr><td><strong>Surprise</strong></td><td>0.914</td><td>0.927</td><td>0.921</td><td>150</td><td>139</td><td>13</td><td>11</td><td>887</td></tr>
            </tbody>
        </table>
    </div>

    <div class="footer">
        Neural Ecosystem R&D Suite — Benchmark Report Generated July 2026
    </div>

</body>
</html>
"""

html_file = os.path.abspath(r"d:\college\DL 4 models\all_models_metrics_report.html")
pdf_file = os.path.abspath(r"d:\college\DL 4 models\all_models_metrics_report.pdf")

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generated at: {html_file}")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_file}",
    f"file:///{html_file.replace('\\', '/')}"
]

print("Executing Edge print-to-pdf...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
if os.path.exists(pdf_file):
    print(f"SUCCESS! PDF created at: {pdf_file} (Size: {os.path.getsize(pdf_file)} bytes)")
else:
    print("FAILED to create PDF.")
