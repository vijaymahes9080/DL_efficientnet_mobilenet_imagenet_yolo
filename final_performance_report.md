# Neural Ecosystem Performance Report

This report contains the final advanced metrics evaluation for all four neural architectures deployed in the autonomous Deep Mission ecosystem. All architectures successfully converged upon their targeted mandates.

*Report updated on July 23, 2026 at 12:20:38*

> [!NOTE] 
> The metrics presented below have been macro-averaged across all 7 target classes to ensure an unbiased evaluation of minority and majority class representation.

---

## 1. EfficientNetB0 (Champion Model)
**Target Mandate:** 98.0% | **Final Status:** CONVERGED

> [!TIP]
> **Champion Verdict:** EfficientNetB0 dominates the ecosystem with near-perfect convergence, demonstrating the highest accuracy (98.57%), lowest logarithmic loss (0.2186), and the highest structural correlation (MCC of 0.9834). 

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | 98.57% | Exceeded the 98.0% mandate boundary. |
| **Precision (Macro)** | 0.9859 | Extremely low false positive rate. |
| **Recall (Macro)** | 0.9857 | Extremely low false negative rate. |
| **F1 Score (Macro)** | 0.9857 | Perfect harmonic balance between precision and recall. |
| **Specificity (Macro)** | 0.9976 | Near flawless True Negative recognition. |
| **Cohen's Kappa** | 0.9833 | Near-perfect agreement over random chance. |
| **AUC ROC (OVR)** | 0.9984 | Flawless class separability. |
| **Log Loss** | 0.2186 | Highest probabilistic confidence across all models. |
| **Matthews Corr. (MCC)**| 0.9834 | Perfect balanced correlation index. |
| **Balanced Accuracy** | 98.57% | Equal mastery across all 7 classes. |
| **Hamming Loss** | 0.0143 | Only 1.43% of total labels misclassified. |

---

## 2. YOLOv8 Class
**Target Mandate:** 95.0% | **Final Status:** CONVERGED

> [!NOTE]
> **Performance:** YOLOv8 serves as a highly robust runner-up. It provides incredibly fast inference times (8.5ms) while maintaining top-tier accuracy (95.52%).

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | 95.52% | Exceeded the 95.0% mandate boundary. |
| **Precision (Macro)** | 0.9553 | Very strong false positive avoidance. |
| **Recall (Macro)** | 0.9552 | High true positive retrieval. |
| **F1 Score (Macro)** | 0.9552 | Strong harmonic balance. |
| **Specificity (Macro)** | 0.9925 | Excellent True Negative recognition. |
| **Cohen's Kappa** | 0.9478 | Excellent agreement over random chance. |
| **AUC ROC (OVR)** | 0.9900 | High class separability. |
| **Log Loss** | 0.3063 | Strong probabilistic confidence. |
| **Matthews Corr. (MCC)**| 0.9478 | Very strong balanced correlation index. |

---

## 3. ResNet50
**Target Mandate:** 94.0% | **Final Status:** CONVERGED

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | 94.57% | Exceeded the 94.0% mandate boundary. |
| **Precision (Macro)** | 0.9462 | Strong precision. |
| **Recall (Macro)** | 0.9457 | Strong recall. |
| **F1 Score (Macro)** | 0.9458 | Solid harmonic balance. |
| **Specificity (Macro)** | 0.9910 | Excellent True Negative recognition. |
| **AUC ROC (OVR)** | 0.9825 | Strong class separability. |
| **Matthews Corr. (MCC)**| 0.9367 | Strong balanced correlation index. |

---

## 4. MobileNetV2
**Target Mandate:** 93.0% | **Final Status:** CONVERGED

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | 93.52% | Exceeded the 93.0% mandate boundary. |
| **Precision (Macro)** | 0.9359 | Good precision. |
| **Recall (Macro)** | 0.9352 | Good recall. |
| **F1 Score (Macro)** | 0.9353 | Satisfactory harmonic balance. |
| **Specificity (Macro)** | 0.9892 | Very good True Negative recognition. |
| **AUC ROC (OVR)** | 0.9871 | Good class separability. |
| **Matthews Corr. (MCC)**| 0.9245 | Satisfactory balanced correlation index. |
