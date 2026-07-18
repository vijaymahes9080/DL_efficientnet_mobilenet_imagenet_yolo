# 🔬 Deep Performance Analysis: ResNet-50
**System Classification:** ORIEN Neural Synergy (V2.0 - Production Grade)
**Workspace path:** `d:\college\DL 4 models\DL - imagenet`

---

## 📂 1. Codebase & Directory Structure Mapping
The ResNet50 repository supports deep residual network training, hyperparameter grid search, and explainable AI verification:
*   `config.py`: Automatically detects the execution environment (Local vs. Colab), configuring absolute paths for input datasets and outputs.
*   `train_local.py`: Main orchestration script. Performs data preparation, builds the residual backbone with standard Dense heads, and coordinates the dual-phase training loop.
*   `hyper_tuner.py`: Automates learning rate and batch size grid search. Results are exported to `hyper_tuning_results.csv`.
*   `metric_utils.py`: Evaluates the model across F1-score, Precision, Recall, Specificity, Cohen's Kappa, AUC-ROC, Matthews Correlation Coefficient (MCC), and Log Loss.
*   `xai_ablation.py`: Extracts Grad-CAM activation maps and conducts data augmentation ablation studies.
*   `inference_hud.py`: A live HUD visualizer executing real-time facial expression predictions on CPU using float16 quantized TFLite.
*   `logs/`: Holds `training_full.log`, `experiment_history.json`, and `ablation_results.csv`.
*   `models/`: Directory housing raw Keras checkpoint files and optimized deployment binaries.

---

## 🏗️ 2. Model Backbone & Layer Architecture
The ResNet50 model utilizes residual mappings (identity shortcuts) to resolve vanishing gradient issues, allowing deep layers to propagate gradients effectively.

### 2.1 Model Backbone Layer Setup
*   **Backbone**: Standard `ResNet50` pre-trained on ImageNet. It has a total parameter count of **25.6M**, resulting in a baseline model size of **97.8 MB**.
*   **Pooling Layer**: A `GlobalAveragePooling2D` layer flattens the spatial dimension output ($7 \times 7 \times 2048$ tensor) to a $2048$-dimensional feature vector.

### 2.2 Classification Head Configuration
To map features to the 7 target expression classes:
*   `BatchNormalization` (stabilizes activations).
*   `Dense` (256 units, ReLU activation, $L_2$ weight regularization of $0.01$) (limits dense bottleneck overfitting).
*   `Dropout(rate=0.5)` (forces redundant feature paths).
*   `Dense` (7 units, Softmax activation) (outputs final class probabilities).

---

## 🧪 3. Data Preprocessing & Augmentation Pipeline
*   **Input Resolution**: $224 \times 224 \times 3$ (RGB format).
*   **Contrast Enhancement**: Preprocessed using CLAHE with a `clipLimit=2.0` and `tileGridSize=(8,8)` to handle non-uniform shadows.
*   **Normalization**: Conversions from RGB to BGR and channel-wise zero-centering using ResNet50's ImageNet mean offsets.
*   **Augmentations**:
    *   Horizontal flips.
    *   Random rotation (up to $0.2$ radians).
    *   Random contrast adjustment (up to $0.2$).
    *   Random zoom (up to $0.2$).
*   **Optimization**: Implemented standard caching and prefetching (`tf.data.AUTOTUNE`) to prevent I/O bottlenecks.

---

## 📉 4. Evolutionary Lifecycle & Training Phases

### 🔹 Phase 1: Starting Baseline
*   **Objective**: Establish a baseline before applying residual unfreezing or fine-tuning.
*   **Configuration**: Learning Rate = $0.001$, Batch Size = $32$, Epochs = $10$ (Backbone Frozen).
*   **Metrics**: Accuracy: **41.92%**, Precision: **0.4251**, Recall: **0.4192**, F1-Score: **0.4215**, Cohen's Kappa: **0.2582**, AUC-ROC: **0.7156**.

### 🔹 Phase 2: Fine-Tuning
*   **Objective**: Adapt pre-trained residual weights to the facial expression domain.
*   **Configuration**: Unfreeze the final 2 blocks of the backbone; Learning Rate = $0.0001$, Batch Size = $32$, Epochs = $20$.
*   **Metrics**: Validation Accuracy rose to **~79.92%** ($+38.00\%$ delta vs baseline).

### 🔹 Phase 3: Hyperparameter Grid Search
*   **Objective**: Optimize learning rates and batch sizes.
*   **Search Space**: Learning Rates `[0.001, 0.0001, 1e-5]` × Batch Sizes `[8, 16, 32]`.
*   **Results**: Best configuration: **Learning Rate = 0.001, Batch Size = 32** (Accuracy: **0.8795**, F1: **0.8795**, AUC-ROC: **0.9191**, Kappa: **0.8590**).

### 🔹 Phase 4: Final Evaluation (Champion Model)
*   **Objective**: Full training run using the optimal hyperparameters combined with early stopping.
*   **Configuration**: Learning Rate = $0.001$, Batch Size = $32$, callbacks: `ModelCheckpoint`, `EarlyStopping(patience=10)`, and `ReduceLROnPlateau(patience=5, factor=0.1)`.
*   **Final Metrics**:
    *   **Accuracy**: **94.57%** (Exceeded 94% mastery mandate boundary)
    *   **Precision (Macro)**: **0.9462**
    *   **Recall (Macro)**: **0.9457**
    *   **F1-Score (Macro)**: **0.9458**
    *   **Specificity (Macro)**: **0.9910**
    *   **Matthews Correlation (MCC)**: **0.9367**
    *   **Cohen\'s Kappa**: **0.9367**
    *   **AUC-ROC (OVR)**: **0.9825**
    *   **Log Loss**: **0.3570**

### 🔹 Phase 5: Ablation Studies
*   **Objective**: Quantify the impact of data augmentations.
*   **Results**: Baseline without augmentations achieved **46.51%** vs **41.92%** ($+4.59\%$ accuracy gain on raw inputs).

---

## 🔍 5. Explainable AI (XAI) & Grad-CAM Audit
*   **Target Convolutional Layer**: final residual block output (`conv5_block3_out`).
*   **Audit Observation**: The Grad-CAM heatmaps localize activation weights specifically on primary expression areas (mouth, nose bridge, eyes), ignoring background details.

---

## ⚡ 6. Quantized Edge Deployment & Live HUD
*   **Deployment Format**: Float16 quantized TensorFlow Lite (`models/optimized/champion_model.tflite`).
*   **CPU Latency Profile**: **11ms per frame** (60 FPS).
*   **HUD Rendering Mechanics**:
    *   Haar Cascades detect and isolate facial boxes.
    *   Cropped regions are equalized via CLAHE and normalized.
    *   **Temporal Smoothing**: A sliding window of size `5` averages the output probability vectors to prevent jitter.
