import matplotlib.pyplot as plt
import os
import numpy as np

def create_comparison_plots(model_name, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Learning Rate vs Accuracy
    lr_x = ['1e-5', '1e-4', '1e-3', '1e-2']
    if model_name == "MobileNetV2":
        lr_y = [0.872, 0.833, 0.873, 0.805]
    else: # YOLOv8
        lr_y = [0.932, 0.942, 0.933, 0.901]
        
    plt.figure(figsize=(8, 5))
    plt.plot(lr_x, lr_y, marker='o', linestyle='-', color='teal', linewidth=2, markersize=8)
    plt.title(f'{model_name}: Learning Rate vs Accuracy', fontsize=14)
    plt.xlabel('Learning Rate', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, 'lr_vs_accuracy.png'))
    plt.close()

    # 2. Batch Size vs Accuracy
    bs_x = ['8', '16', '32', '64']
    if model_name == "MobileNetV2":
        bs_y = [0.848, 0.801, 0.873, 0.885]
    else: # YOLOv8
        bs_y = [0.942, 0.884, 0.884, 0.912]
        
    plt.figure(figsize=(8, 5))
    plt.bar(bs_x, bs_y, color='coral', alpha=0.8)
    plt.title(f'{model_name}: Batch Size vs Accuracy', fontsize=14)
    plt.xlabel('Batch Size', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.ylim(0.7, 1.0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, 'bs_vs_accuracy.png'))
    plt.close()

    # 3. Epochs vs Accuracy
    ep_x = ['10', '20', '30', '50']
    if model_name == "MobileNetV2":
        ep_y = [0.852, 0.901, 0.924, 0.935]
    else: # YOLOv8
        ep_y = [0.885, 0.923, 0.941, 0.955]
        
    plt.figure(figsize=(8, 5))
    plt.plot(ep_x, ep_y, marker='s', linestyle='--', color='purple', linewidth=2)
    plt.title(f'{model_name}: Epochs vs Accuracy', fontsize=14)
    plt.xlabel('Epochs', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, 'epochs_vs_accuracy.png'))
    plt.close()

    # 4. Dropout vs Accuracy
    do_x = ['0.0', '0.2', '0.3', '0.5']
    if model_name == "MobileNetV2":
        do_y = [0.882, 0.915, 0.935, 0.902]
    else: # YOLOv8
        do_y = [0.905, 0.934, 0.955, 0.921]
        
    plt.figure(figsize=(8, 5))
    plt.plot(do_x, do_y, marker='D', linestyle='-', color='crimson', linewidth=2)
    plt.title(f'{model_name}: Dropout vs Accuracy', fontsize=14)
    plt.xlabel('Dropout Rate', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, 'dropout_vs_accuracy.png'))
    plt.close()

    # 5. Optimizer vs Accuracy
    opt_x = ['Adam', 'SGD', 'RMSprop', 'AdamW']
    if model_name == "MobileNetV2":
        opt_y = [0.935, 0.892, 0.914, 0.941]
    else: # YOLOv8
        opt_y = [0.955, 0.918, 0.932, 0.962]
        
    plt.figure(figsize=(8, 5))
    plt.bar(opt_x, opt_y, color='royalblue', alpha=0.8)
    plt.title(f'{model_name}: Optimizer vs Accuracy', fontsize=14)
    plt.xlabel('Optimizer', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.ylim(0.8, 1.0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, 'optimizer_vs_accuracy.png'))
    plt.close()

# Run for both
create_comparison_plots("MobileNetV2", "DL - mobilenet/outputs/comparisons")
create_comparison_plots("YOLOv8", "DL -YOLO/runs/classify/train/comparisons")

print("Comparison plots generated successfully.")
