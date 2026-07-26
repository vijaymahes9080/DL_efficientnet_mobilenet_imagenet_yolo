import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_flowchart(models_list, filename, title_suffix=""):
    fig, ax = plt.subplots(figsize=(9, 14), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Style definitions matching reference image
    pink_color = '#FADBD8'      # Soft pinkish background for main boxes
    pink_border = '#E6B0AA'
    purple_color = '#E8DAEF'    # Soft purple background for model boxes
    purple_border = '#D2B4DE'
    text_color = '#1A1A1A'
    subtext_color = '#333333'
    arrow_color = '#2C3E50'

    # Node definitions: (x_center, y_center, width, height, title, subtitle, color, border)
    nodes = [
        (0.5, 0.94, 0.45, 0.05, "Data Collection", "", pink_color, pink_border),
        (0.5, 0.84, 0.65, 0.06, "Preprocessing", "resize, RGB conversion, normalisation", pink_color, pink_border),
        (0.5, 0.74, 0.45, 0.05, "Data Augmentation", "", pink_color, pink_border),
        (0.5, 0.64, 0.48, 0.06, "Model Development", "build_model", pink_color, pink_border),
    ]

    # Model nodes (Row of 4)
    model_y = 0.50
    model_w = 0.20
    model_h = 0.055
    model_xs = [0.125, 0.375, 0.625, 0.875]

    for m_name, m_x in zip(models_list, model_xs):
        nodes.append((m_x, model_y, model_w, model_h, m_name, "", purple_color, purple_border))

    # Bottom sequential nodes
    nodes.extend([
        (0.5, 0.36, 0.48, 0.05, "Hyperparameter Tuning", "", pink_color, pink_border),
        (0.5, 0.26, 0.42, 0.05, "Fine-Tuning", "", pink_color, pink_border),
        (0.5, 0.16, 0.48, 0.06, "Explainable AI", "Grad-CAM, LIME", pink_color, pink_border),
        (0.5, 0.06, 0.42, 0.05, "Ablation Study", "", pink_color, pink_border),
    ])

    # Draw Boxes & Text
    box_dict = {}
    for node in nodes:
        cx, cy, w, h, title, sub, bg, border = node
        x = cx - w/2
        y = cy - h/2
        
        # Fancy box shape
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="square,pad=0",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.5,
            zorder=3
        )
        ax.add_patch(rect)

        # Text rendering
        if sub:
            ax.text(cx, cy + 0.008, title, ha='center', va='center', fontsize=11, fontweight='bold', color=text_color, zorder=4)
            ax.text(cx, cy - 0.012, sub, ha='center', va='center', fontsize=9.5, fontweight='normal', color=subtext_color, zorder=4)
        else:
            ax.text(cx, cy, title, ha='center', va='center', fontsize=11, fontweight='bold', color=text_color, zorder=4)

        box_dict[title] = (cx, cy, w, h)

    # Helper function for arrows
    def draw_arrow(start_pos, end_pos, connectionstyle="arc3,rad=0"):
        ax.annotate(
            '', xy=end_pos, xytext=start_pos,
            arrowprops=dict(
                arrowstyle="-|>",
                color=arrow_color,
                lw=1.8,
                mutation_scale=14,
                connectionstyle=connectionstyle
            ),
            zorder=2
        )

    # Sequential Arrows (Top part)
    # Data Collection -> Preprocessing
    draw_arrow((0.5, 0.94 - 0.025), (0.5, 0.84 + 0.03))
    # Preprocessing -> Data Augmentation
    draw_arrow((0.5, 0.84 - 0.03), (0.5, 0.74 + 0.025))
    # Data Augmentation -> Model Development
    draw_arrow((0.5, 0.74 - 0.025), (0.5, 0.64 + 0.03))

    # Model Development -> 4 Models (Branching)
    dev_bottom_y = 0.64 - 0.03
    for m_x in model_xs:
        m_top_y = model_y + model_h/2
        # Orthogonal / clean line to model box
        ax.plot([0.5, m_x], [dev_bottom_y - 0.02, dev_bottom_y - 0.02], color=arrow_color, lw=1.8, zorder=2)
        ax.plot([0.5, 0.5], [dev_bottom_y, dev_bottom_y - 0.02], color=arrow_color, lw=1.8, zorder=2)
        draw_arrow((m_x, dev_bottom_y - 0.02), (m_x, m_top_y))

    # 4 Models -> Hyperparameter Tuning (Merging)
    tune_top_y = 0.36 + 0.025
    for m_x in model_xs:
        m_bottom_y = model_y - model_h/2
        ax.plot([m_x, m_x], [m_bottom_y, tune_top_y + 0.02], color=arrow_color, lw=1.8, zorder=2)
        ax.plot([m_x, 0.5], [tune_top_y + 0.02, tune_top_y + 0.02], color=arrow_color, lw=1.8, zorder=2)
    draw_arrow((0.5, tune_top_y + 0.02), (0.5, tune_top_y))

    # Sequential Arrows (Bottom part)
    # Hyperparameter Tuning -> Fine-Tuning
    draw_arrow((0.5, 0.36 - 0.025), (0.5, 0.26 + 0.025))
    # Fine-Tuning -> Explainable AI
    draw_arrow((0.5, 0.26 - 0.025), (0.5, 0.16 + 0.03))
    # Explainable AI -> Ablation Study
    draw_arrow((0.5, 0.16 - 0.03), (0.5, 0.06 + 0.025))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved flowchart to {filename}")

if __name__ == "__main__":
    # Flowchart with MOBILENETV2, YOLOV8, RESNET50, EFFICIENTNETB0
    models_list = ["MOBILENETV2", "YOLOV8", "RESNET50", "EFFICIENTNETB0"]
    create_flowchart(models_list, "proposed_models_flowchart.png")
    print("Updated proposed_models_flowchart.png with MOBILENETV2, YOLOV8, RESNET50, EFFICIENTNETB0")


