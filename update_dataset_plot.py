import os
import matplotlib.pyplot as plt
import numpy as np

def generate_balanced_dataset_plot():
    # Set dark/modern aesthetic to match presentation
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
    
    classes = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    raw_counts = [1186, 460, 1188, 1197, 1194, 1189, 1115]
    
    # Calculate inverse class weights
    total_samples = sum(raw_counts) # 7529
    num_classes = len(classes)      # 7
    class_weights = [total_samples / (num_classes * n) for n in raw_counts]
    effective_balanced_counts = [round(n * w) for n, w in zip(raw_counts, class_weights)] # 1076 for all
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    
    for ax in [ax1, ax2]:
        ax.set_facecolor('#1E293B')
        ax.tick_params(colors='#F8FAFC', labelsize=10)
        ax.xaxis.label.set_color('#F8FAFC')
        ax.yaxis.label.set_color('#F8FAFC')
        ax.title.set_color('#38BDF8')
        ax.grid(True, linestyle='--', alpha=0.3, color='#516585')
        
    # Panel 1: Raw Imbalanced Distribution
    colors_raw = ['#38BDF8', '#A855F7', '#38BDF8', '#38BDF8', '#38BDF8', '#38BDF8', '#F59E0B']
    bars1 = ax1.bar(classes, raw_counts, color=colors_raw, width=0.55, edgecolor='#334155', linewidth=1.5)
    ax1.set_title('Raw Dataset Distribution (Imbalanced Disgust: 460)', fontsize=12, fontweight='bold', pad=12)
    ax1.set_ylabel('Number of Images', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 1400)
    
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 25, f'{int(yval)}', ha='center', va='bottom', 
                 color='#F8FAFC', fontweight='bold', fontsize=10)
        
    # Highlight Disgust Imbalance Callout
    ax1.annotate('Minority Imbalance\n(460 Samples)', xy=(1, 460), xytext=(1, 750),
                 arrowprops=dict(facecolor='#A855F7', shrink=0.08, width=2, headwidth=8),
                 color='#A855F7', fontweight='bold', fontsize=10, ha='center',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#A855F7', lw=1.5))
        
    # Panel 2: Effective Balanced Distribution (Inverse Class Weighting + CLAHE)
    colors_bal = ['#34D399'] * num_classes
    bars2 = ax2.bar(classes, effective_balanced_counts, color=colors_bal, width=0.55, edgecolor='#334155', linewidth=1.5)
    ax2.set_title('Balanced Pipeline Effective Distribution (w_c Class Weighting)', fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylabel('Effective Weighted Impact (Samples)', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 1400)
    
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 25, f'{int(yval)}', ha='center', va='bottom', 
                 color='#34D399', fontweight='bold', fontsize=10)
        
    # Balance Line Indicator
    ax2.axhline(1076, color='#FBBF24', linestyle='--', linewidth=2, label='Target Balance Level (1076)')
    ax2.legend(loc='upper right', facecolor='#1E293B', edgecolor='#FBBF24', labelcolor='#F8FAFC')

    plt.suptitle('Fig. 1 | Dataset Balancing Protocol: Raw Imbalanced vs Effective Weight Balancing', 
                 fontsize=14, fontweight='bold', color='#F8FAFC', y=0.98)
    plt.tight_layout()
    
    out_path = r"d:\college\DL 4 models\zz paper\figures\fig1_dataset.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Successfully updated balanced dataset figure at: {out_path}")

if __name__ == "__main__":
    generate_balanced_dataset_plot()
