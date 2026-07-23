import matplotlib.pyplot as plt
import numpy as np
import os

# Set aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

models = ['Fused EfficientNet-B0\n(🏆 Champion)', 'YOLOv8 Class\n(Runner-up)', 'ResNet50', 'MobileNetV2']
colors = ['#10B981', '#2563EB', '#0D9488', '#F59E0B']

# Data Metrics
accuracy = [98.57, 95.52, 94.57, 93.52]
f1_macro = [0.9857, 0.9552, 0.9458, 0.9353]
precision = [0.9859, 0.9553, 0.9462, 0.9359]
recall = [0.9857, 0.9552, 0.9457, 0.9352]
specificity = [0.9976, 0.9925, 0.9910, 0.9892]
mcc = [0.9834, 0.9478, 0.9367, 0.9245]
kappa = [0.9833, 0.9478, 0.9367, 0.9244]
log_loss = [0.2186, 0.3063, 0.3570, 0.3533]
ece_pct = [1.85, 3.21, 4.12, 4.89]
latency_ms = [11.0, 6.8, 15.4, 5.9]
model_size_mb = [20.3, 10.5, 97.8, 9.6]
params_m = [5.33, 2.72, 25.64, 2.26]
roc_auc = [0.9984, 0.9900, 0.9825, 0.9871]
auprc = [0.9978, 0.9856, 0.9782, 0.9745]

# Per-Class F1-Scores
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
f1_per_class = {
    'Fused EfficientNet-B0 (🏆)': [0.980, 0.983, 0.993, 0.990, 0.987, 0.977, 0.990],
    'YOLOv8 Class (Runner-up)': [0.949, 0.947, 0.952, 0.953, 0.947, 0.964, 0.974],
    'ResNet50': [0.947, 0.950, 0.957, 0.946, 0.950, 0.944, 0.926],
    'MobileNetV2': [0.924, 0.936, 0.941, 0.943, 0.927, 0.956, 0.921]
}

fig = plt.figure(figsize=(18, 12))
fig.suptitle('🏆 Neural Ecosystem: 4-Model Visual Comparison Dashboard', fontsize=20, fontweight='bold', color='#0F172A', y=0.98)

# 1. Accuracy & F1-Score Bar Chart
ax1 = fig.add_subplot(2, 3, 1)
x = np.arange(len(models))
width = 0.35
rects1 = ax1.bar(x - width/2, accuracy, width, label='Accuracy (%)', color='#2563EB', alpha=0.9, edgecolor='#1E3A8A')
rects2 = ax1.bar(x + width/2, [f * 100 for f in f1_macro], width, label='F1-Score (%)', color='#10B981', alpha=0.9, edgecolor='#065F46')
ax1.set_ylabel('Percentage (%)', fontweight='bold', fontsize=11)
ax1.set_title('1. Classification Accuracy & F1-Score', fontweight='bold', fontsize=13, color='#0F172A')
ax1.set_xticks(x)
ax1.set_xticklabels(models, fontsize=9.5)
ax1.set_ylim(85, 101)
ax1.legend(loc='lower right', frameon=True)
for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'{h:.2f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'{h:.2f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

# 2. Log Loss & Expected Calibration Error (ECE)
ax2 = fig.add_subplot(2, 3, 2)
rects3 = ax2.bar(x - width/2, log_loss, width, label='Logarithmic Loss', color='#DC2626', alpha=0.85, edgecolor='#7F1D1D')
ax2_twin = ax2.twinx()
rects4 = ax2_twin.bar(x + width/2, ece_pct, width, label='ECE Calibration Error (%)', color='#F59E0B', alpha=0.85, edgecolor='#92400E')
ax2.set_ylabel('Log Loss (Lower is Better)', fontweight='bold', fontsize=10, color='#DC2626')
ax2_twin.set_ylabel('ECE Error % (Lower is Better)', fontweight='bold', fontsize=10, color='#F59E0B')
ax2.set_title('2. Loss & Calibration Error (Lower is Better)', fontweight='bold', fontsize=13, color='#0F172A')
ax2.set_xticks(x)
ax2.set_xticklabels(models, fontsize=9.5)
ax2.set_ylim(0, 0.5)
ax2_twin.set_ylim(0, 7)
for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#7F1D1D')
for rect in rects4:
    h = rect.get_height()
    ax2_twin.annotate(f'{h:.2f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#92400E')

# 3. Hardware Efficiency Scatter (Latency vs Model Size)
ax3 = fig.add_subplot(2, 3, 3)
for i in range(len(models)):
    ax3.scatter(latency_ms[i], model_size_mb[i], s=params_m[i]*40 + 200, color=colors[i], alpha=0.8, edgecolors='#0F172A', linewidth=1.5, zorder=5)
    ax3.annotate(f"{models[i].splitlines()[0]}\n({latency_ms[i]}ms, {model_size_mb[i]}MB)", (latency_ms[i]+0.4, model_size_mb[i]), fontsize=8.5, fontweight='bold')
ax3.set_xlabel('CPU Inference Latency (ms / frame)', fontweight='bold', fontsize=11)
ax3.set_ylabel('Model File Size (MB)', fontweight='bold', fontsize=11)
ax3.set_title('3. Latency vs Size Efficiency Trade-off', fontweight='bold', fontsize=13, color='#0F172A')
ax3.set_xlim(4, 18)
ax3.set_ylim(0, 115)
ax3.grid(True, linestyle='--', alpha=0.6)

# 4. Per-Class F1-Score Heatmap / Grouped Bar
ax4 = fig.add_subplot(2, 3, 4)
x_emo = np.arange(len(emotions))
w_bar = 0.2
for idx, (m_label, f1_vals) in enumerate(f1_per_class.items()):
    ax4.bar(x_emo + (idx - 1.5)*w_bar, [v * 100 for v in f1_vals], w_bar, label=m_label.splitlines()[0], color=colors[idx], alpha=0.85)
ax4.set_ylabel('F1-Score (%)', fontweight='bold', fontsize=11)
ax4.set_title('4. Per-Class F1-Score Breakdown (7 Emotions)', fontweight='bold', fontsize=13, color='#0F172A')
ax4.set_xticks(x_emo)
ax4.set_xticklabels(emotions, fontsize=9.5, fontweight='bold')
ax4.set_ylim(90, 101)
ax4.legend(loc='lower right', fontsize=8, frameon=True)

# 5. ROC-AUC & AUPRC Comparison
ax5 = fig.add_subplot(2, 3, 5)
rects5 = ax5.bar(x - width/2, roc_auc, width, label='ROC-AUC (OVR)', color='#8B5CF6', alpha=0.85, edgecolor='#4C1D95')
rects6 = ax5.bar(x + width/2, auprc, width, label='AUPRC', color='#06B6D4', alpha=0.85, edgecolor='#155E75')
ax5.set_ylabel('Area Under Curve Score', fontweight='bold', fontsize=11)
ax5.set_title('5. ROC-AUC & Precision-Recall AUC (AUPRC)', fontweight='bold', fontsize=13, color='#0F172A')
ax5.set_xticks(x)
ax5.set_xticklabels(models, fontsize=9.5)
ax5.set_ylim(0.96, 1.002)
ax5.legend(loc='lower right', frameon=True)
for rect in rects5:
    h = rect.get_height()
    ax5.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
for rect in rects6:
    h = rect.get_height()
    ax5.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

# 6. Matthews Correlation (MCC) & Cohen's Kappa Score
ax6 = fig.add_subplot(2, 3, 6)
rects7 = ax6.bar(x - width/2, mcc, width, label='MCC Index', color='#10B981', alpha=0.85, edgecolor='#065F46')
rects8 = ax6.bar(x + width/2, kappa, width, label="Cohen's Kappa", color='#3B82F6', alpha=0.85, edgecolor='#1E3A8A')
ax6.set_ylabel('Correlation / Agreement Index', fontweight='bold', fontsize=11)
ax6.set_title('6. MCC & Cohen\'s Kappa Statistical Agreement', fontweight='bold', fontsize=13, color='#0F172A')
ax6.set_xticks(x)
ax6.set_xticklabels(models, fontsize=9.5)
ax6.set_ylim(0.90, 1.002)
ax6.legend(loc='lower right', frameon=True)
for rect in rects7:
    h = rect.get_height()
    ax6.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
for rect in rects8:
    h = rect.get_height()
    ax6.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.96])

out_png = r"d:\college\DL 4 models\master_4_models_visual_comparison.png"
plt.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"SUCCESS: Comparison chart saved to {out_png}")
plt.close()
