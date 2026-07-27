import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def build_xai_grid():
    base_dir = r"d:\college\DL 4 models"
    
    # Locate existing XAI images
    resnet_xai_dir = os.path.join(base_dir, "DL - imagenet", "outputs", "xai")
    eff_xai_dir = os.path.join(base_dir, "DL - efficientnet b0", "outputs", "xai")
    
    resnet_imgs = sorted([os.path.join(resnet_xai_dir, f) for f in os.listdir(resnet_xai_dir) if f.endswith('.png')])
    eff_imgs = sorted([os.path.join(eff_xai_dir, f) for f in os.listdir(eff_xai_dir) if f.endswith('.png')])
    
    print(f"Found {len(resnet_imgs)} ResNet XAI images and {len(eff_imgs)} EfficientNet XAI images.")
    
    fig, axes = plt.subplots(3, 2, figsize=(14, 11), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    
    # Title
    fig.suptitle('Explainable AI (XAI) Master Audit & Visual Attention Analysis\nGrad-CAM Heatmaps & Occlusion Sensitivity across Neural Ecosystem', 
                 fontsize=15, fontweight='bold', color='#F8FAFC', y=0.97)

    plot_items = [
        ("ResNet50 — Class: Happy (Grad-CAM & Occlusion)", resnet_imgs[3] if len(resnet_imgs) > 3 else resnet_imgs[0]),
        ("ResNet50 — Class: Angry (Grad-CAM & Occlusion)", resnet_imgs[0]),
        ("ResNet50 — Class: Fear (Grad-CAM & Occlusion)", resnet_imgs[2] if len(resnet_imgs) > 2 else resnet_imgs[0]),
        ("ResNet50 — Class: Neutral (Grad-CAM & Occlusion)", resnet_imgs[4] if len(resnet_imgs) > 4 else resnet_imgs[0]),
        ("EfficientNet-B0 — Champion Class Focus (Grad-CAM)", eff_imgs[0] if len(eff_imgs) > 0 else resnet_imgs[0]),
        ("EfficientNet-B0 — Multi-Scale AU Focus", eff_imgs[1] if len(eff_imgs) > 1 else resnet_imgs[1]),
    ]

    for ax, (title, img_path) in zip(axes.flatten(), plot_items):
        ax.set_facecolor('#1E293B')
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax.imshow(img)
        ax.set_title(title, fontsize=11, fontweight='bold', color='#38BDF8', pad=8)
        ax.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.93])

    out1 = os.path.join(base_dir, "xai_master_comparison_grid.png")
    artifact_dir = r"C:\Users\vijay\.gemini\antigravity-ide\brain\874ede44-9eeb-45bd-9035-1280be1e28e5"
    out2 = os.path.join(artifact_dir, "xai_master_comparison_grid.png")

    plt.savefig(out1, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.savefig(out2, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    print(f"Saved XAI Master Comparison Grid:\n 1. {out1}\n 2. {out2}")

if __name__ == "__main__":
    build_xai_grid()
