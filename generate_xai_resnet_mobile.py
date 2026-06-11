"""
generate_xai_resnet_mobile.py
Generates Grad-CAM + Occlusion Sensitivity XAI reports for ResNet50 and MobileNetV2.
Saves per-class XAI images to each model's outputs/xai/ directory.
Run from: d:\\DL 4 models\\
"""

import os
import sys
import cv2
import numpy as np

# Suppress TF noise before importing TF
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tensorflow.keras import models as keras_models
from tensorflow.keras.layers import BatchNormalization

# ---------------------------------------------------------------------------
# Monkey-patch BatchNormalization.from_config to tolerate old TF2-saved models
# that include 'renorm' kwargs which newer Keras does not accept.
# Patching from_config (not __init__) is required because Keras reconstructs
# nested layers via from_config(), bypassing custom_objects entirely.
# ---------------------------------------------------------------------------
_original_bn_from_config = BatchNormalization.from_config.__func__

@classmethod  # type: ignore[misc]
def _patched_bn_from_config(cls, config):
    for k in ('renorm', 'renorm_clipping', 'renorm_momentum'):
        config.pop(k, None)
    return _original_bn_from_config(cls, config)

BatchNormalization.from_config = _patched_bn_from_config  # type: ignore[assignment]


# ─── Last Conv Layer Names ────────────────────────────────────────────────────
LAST_CONV_LAYERS = {
    'resnet':  'conv5_block3_out',       # ResNet50 final residual block output
    'mobile':  'Conv_1',                 # MobileNetV2 final conv
}

MODEL_CONFIGS = {
    'resnet': {
        'folder':     r'd:\DL 4 models\DL - imagenet',
        'model_file': r'models\champion_model_mastery.keras',
        'dataset':    r'dataset',
        'xai_out':    r'outputs\xai',
        'label':      'ResNet50',
    },
    'mobile': {
        'folder':     r'd:\DL 4 models\DL - mobilenet',
        'model_file': r'models\champion_model_mastery.keras',
        'dataset':    r'dataset',
        'xai_out':    r'outputs\xai',
        'label':      'MobileNetV2',
    },
}

# ─── XAI Functions ────────────────────────────────────────────────────────────

def get_gradcam_heatmap(model, img_array, last_conv_layer_name):
    """Compute Grad-CAM heatmap via GradientTape."""
    try:
        # Try nested backbone first (Sequential wrapping a functional backbone)
        if hasattr(model.layers[0], 'layers'):
            backbone = model.layers[0]
            try:
                conv_output = backbone.get_layer(last_conv_layer_name).output
                grad_model = keras_models.Model(
                    [backbone.inputs], [conv_output, model.output]
                )
            except Exception:
                # Fallback: search entire model
                grad_model = keras_models.Model(
                    [model.inputs],
                    [model.get_layer(last_conv_layer_name).output, model.output]
                )
        else:
            grad_model = keras_models.Model(
                [model.inputs],
                [model.get_layer(last_conv_layer_name).output, model.output]
            )

        img_tensor = tf.cast(img_array, tf.float32)
        with tf.GradientTape() as tape:
            conv_out, preds = grad_model(img_tensor)
            tape.watch(conv_out)
            pred_class = tf.argmax(preds[0])
            class_channel = preds[:, pred_class]

        grads = tape.gradient(class_channel, conv_out)
        pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
        heatmap = conv_out[0] @ pooled[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        return heatmap.numpy(), int(pred_class.numpy())
    except Exception as e:
        print(f"  [XAI WARN] Grad-CAM failed ({e}), returning zero heatmap")
        return np.zeros((7, 7)), 0


def occlusion_sensitivity(model, img, label, patch_size=32):
    """Compute occlusion sensitivity map."""
    h, w = img.shape[:2]
    heatmap = np.zeros((h, w), dtype=np.float32)
    try:
        baseline = model.predict(np.expand_dims(img, 0), verbose=0)[0][label]
        for i in range(0, h, patch_size):
            for j in range(0, w, patch_size):
                occ = img.copy()
                occ[i:i+patch_size, j:j+patch_size, :] = 0
                new_pred = model.predict(np.expand_dims(occ, 0), verbose=0)[0][label]
                heatmap[i:i+patch_size, j:j+patch_size] = max(0.0, baseline - new_pred)
        if heatmap.max() > 0:
            heatmap /= heatmap.max()
    except Exception as e:
        print(f"  [XAI WARN] Occlusion failed: {e}")
    return heatmap


def save_xai_image(img_raw, gradcam_heatmap, occ_heatmap, class_name, model_label, out_path):
    """Save a 3-panel Grad-CAM + Occlusion figure."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img_disp = (img_raw - img_raw.min()) / (img_raw.max() - img_raw.min() + 1e-8)

    gc_res = cv2.resize(gradcam_heatmap, (img_raw.shape[1], img_raw.shape[0]))

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'{model_label} — XAI Report | Class: {class_name}', fontsize=14, fontweight='bold')

    axes[0].imshow(img_disp)
    axes[0].set_title(f'Original Image\n({class_name})', fontsize=11)

    axes[1].imshow(img_disp)
    axes[1].imshow(gc_res, cmap='jet', alpha=0.5)
    axes[1].set_title('Grad-CAM\n(Focus Regions)', fontsize=11)

    axes[2].imshow(img_disp)
    axes[2].imshow(occ_heatmap, cmap='hot', alpha=0.5)
    axes[2].set_title('Occlusion Sensitivity\n(Critical Patches)', fontsize=11)

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(out_path, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  [XAI] Saved -> {out_path}")


# ─── Main Processing ──────────────────────────────────────────────────────────

def process_model(key):
    cfg = MODEL_CONFIGS[key]
    folder      = cfg['folder']
    model_path  = os.path.join(folder, cfg['model_file'])
    dataset_dir = os.path.join(folder, cfg['dataset'])
    xai_out_dir = os.path.join(folder, cfg['xai_out'])
    model_label = cfg['label']
    last_conv   = LAST_CONV_LAYERS[key]

    print(f"\n{'='*60}")
    print(f" Processing XAI for: {model_label}")
    print(f"{'='*60}")

    # ── Load Model ────────────────────────────────────────────────
    if not os.path.exists(model_path):
        print(f"  [ERROR] Model not found: {model_path}")
        return False

    print(f"  Loading model from {model_path} ...")
    try:
        # from_config is monkey-patched globally to strip renorm kwargs
        model = tf.keras.models.load_model(model_path, compile=False)
    except Exception as e:
        print(f"  [ERROR] Could not load model: {e}")
        return False
    print(f"  Model loaded. Input shape: {model.input_shape}")


    # ── Load samples per class ────────────────────────────────────
    if not os.path.exists(dataset_dir):
        print(f"  [ERROR] Dataset missing: {dataset_dir}")
        return False

    class_names = sorted([
        d for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d))
        and not d.startswith('.')
    ])
    print(f"  Found {len(class_names)} classes: {class_names}")

    os.makedirs(xai_out_dir, exist_ok=True)
    generated = 0

    for class_idx, class_name in enumerate(class_names):
        class_dir = os.path.join(dataset_dir, class_name)
        images = [
            f for f in os.listdir(class_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        if not images:
            print(f"  [SKIP] No images in class: {class_name}")
            continue

        # Pick first available image for this class
        img_path = os.path.join(class_dir, images[0])
        try:
            img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
            img_array = tf.keras.utils.img_to_array(img)   # shape (224,224,3)
            img_batch = np.expand_dims(img_array, 0)        # shape (1,224,224,3)

            print(f"  Processing class [{class_idx}] {class_name} ...")

            # Grad-CAM
            gradcam, pred_class = get_gradcam_heatmap(model, img_batch, last_conv)

            # Occlusion (use true class label)
            occ = occlusion_sensitivity(model, img_array, class_idx)

            # Save
            out_file = os.path.join(xai_out_dir, f"sample_{class_idx}_{class_name}.png")
            save_xai_image(img_array, gradcam, occ, class_name, model_label, out_file)
            generated += 1

        except Exception as e:
            print(f"  [ERROR] class {class_name}: {e}")

    print(f"\n  [SUCCESS] {model_label} XAI complete - {generated}/{len(class_names)} images saved to:")
    print(f"     {xai_out_dir}")
    return generated > 0


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ['resnet', 'mobile']
    valid = [t for t in targets if t in MODEL_CONFIGS]
    if not valid:
        print(f"Usage: python generate_xai_resnet_mobile.py [resnet] [mobile]")
        sys.exit(1)

    results = {}
    for key in valid:
        results[key] = process_model(key)

    print(f"\n{'='*60}")
    print(" XAI Generation Summary")
    print(f"{'='*60}")
    for k, ok in results.items():
        status = "SUCCESS" if ok else "FAILED"
        print(f"  {MODEL_CONFIGS[k]['label']:15s} -> {status}")
    print()
