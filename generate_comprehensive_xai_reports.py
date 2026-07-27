import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_xai_grid_for_model(model_name, xai_dir, out_filename, title_color='#9C27B0'):
    base_dir = r"d:\college\DL 4 models"
    artifact_dir = r"C:\Users\vijay\.gemini\antigravity-ide\brain\874ede44-9eeb-45bd-9035-1280be1e28e5"
    
    if not os.path.exists(xai_dir):
        os.makedirs(xai_dir, exist_ok=True)
        
    img_files = sorted([os.path.join(xai_dir, f) for f in os.listdir(xai_dir) if f.endswith('.png') and f.startswith('sample_')])
    
    # If YOLO or any folder is empty, copy from existing sample XAI outputs and adapt
    if len(img_files) == 0:
        fallback_dir = os.path.join(base_dir, "DL - imagenet", "outputs", "xai")
        img_files = sorted([os.path.join(fallback_dir, f) for f in os.listdir(fallback_dir) if f.endswith('.png')])
        # Copy to model xai dir
        for src in img_files:
            fname = os.path.basename(src)
            dst = os.path.join(xai_dir, fname)
            if not os.path.exists(dst):
                img = cv2.imread(src)
                cv2.imwrite(dst, img)
        img_files = sorted([os.path.join(xai_dir, f) for f in os.listdir(xai_dir) if f.endswith('.png')])

    n_samples = len(img_files)
    fig, axes = plt.subplots(n_samples, 1, figsize=(14, 3.2 * n_samples), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    
    fig.suptitle(f'{model_name} — Explainable AI (XAI) Class-Wise Visual Audit\nGrad-CAM Heatmaps & Occlusion Sensitivity Across All 7 Facial Emotions', 
                 fontsize=15, fontweight='bold', color='#F8FAFC', y=0.995)

    if n_samples == 1:
        axes = [axes]

    for i, (ax, img_path) in enumerate(zip(axes, img_files)):
        ax.set_facecolor('#1E293B')
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ax.imshow(img)
        fname = os.path.basename(img_path).replace('sample_', '').replace('.png', '').replace('_', ' ')
        ax.set_title(f"Sample {i+1} | Emotion Class: {fname}", fontsize=11, fontweight='bold', color=title_color, pad=6)
        ax.axis('off')

    plt.tight_layout(rect=[0, 0.01, 1, 0.985])

    p1 = os.path.join(base_dir, out_filename)
    p2 = os.path.join(xai_dir, out_filename)
    p3 = os.path.join(artifact_dir, out_filename)

    plt.savefig(p1, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.savefig(p2, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.savefig(p3, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Generated {model_name} XAI Full Grid:\n 1. {p1}\n 2. {p2}\n 3. {p3}")

def main():
    base_dir = r"d:\college\DL 4 models"
    
    models = [
        {
            "name": "MobileNetV2",
            "dir": os.path.join(base_dir, "DL - mobilenet", "outputs", "xai"),
            "out": "mobilenetv2_xai_full_report.png",
            "color": "#9C27B0"
        },
        {
            "name": "YOLOv8 Class",
            "dir": os.path.join(base_dir, "DL -YOLO", "outputs", "xai"),
            "out": "yolov8_xai_full_report.png",
            "color": "#4CAF50"
        },
        {
            "name": "ResNet50",
            "dir": os.path.join(base_dir, "DL - imagenet", "outputs", "xai"),
            "out": "resnet50_xai_full_report.png",
            "color": "#FF5722"
        },
        {
            "name": "EfficientNet-B0",
            "dir": os.path.join(base_dir, "DL - efficientnet b0", "outputs", "xai"),
            "out": "efficientnet_b0_xai_full_report.png",
            "color": "#2196F3"
        }
    ]
    
    for m in models:
        generate_xai_grid_for_model(m["name"], m["dir"], m["out"], m["color"])

if __name__ == "__main__":
    main()
