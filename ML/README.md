# 🌾 Fertilizer Requirement Prediction Using Regularized Logistic Regression

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange?logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Validated%20%26%20Colab%20Ready-success)

---

## 👨‍💻 Project Overview & Attribution
- **Authors:** Sai Snehith (2520090149) & Harshith Reddy (2520090114)
- **Department:** Computer Science & Information Technology (CSIT)
- **Academic Year:** 2026–27
- **Primary Method:** Regularized Logistic Regression ($L_1$ Lasso, $L_2$ Ridge, and ElasticNet)

---

## 📂 Included Datasets
This repository includes two production-grade, benchmark agricultural datasets:

1. **[`fertilizer_requirement_dataset.csv`](file:///c:/Users/harsh/OneDrive/Desktop/ML/fertilizer_requirement_dataset.csv)** (2,500 samples, 12 features)
   - **Soil Macro-Nutrients:** `Nitrogen` (N), `Phosphorus` (P), `Potassium` (K) in kg/ha
   - **Soil Chemistry & Texture:** `pH` (acidity/alkalinity), `Soil_Moisture` (%), `Soil_Type` (Clayey, Sandy, Loamy, Black, Red, Laterite)
   - **Climatic Parameters:** `Temperature` (°C), `Humidity` (%), `Rainfall` (mm)
   - **Crop Species:** `Crop_Type` (Rice, Wheat, Maize, Cotton, Sugarcane, Pulses, Barley, Soybean, Groundnut, Mustard)
   - **Target Variable:** `Fertilizer_Required` (Binary: 1 = Required, 0 = Nutrients Adequate)
   - **Nutrient Action:** `Recommended_Fertilizer` (Urea, DAP, MOP, 17-17-17, etc.)

2. **[`fertilizer_prediction_kaggle_benchmark.csv`](file:///c:/Users/harsh/OneDrive/Desktop/ML/fertilizer_prediction_kaggle_benchmark.csv)** (2,500 samples, 10 features)
   - Standardized format compatible with Kaggle's public agricultural benchmark schemas.

---

## 🚀 Running in Google Colab (Zero-Friction Setup)

1. Open **[Google Colab](https://colab.research.google.com/)**.
2. Click **Upload** and select [`Fertilizer_Requirement_Prediction_Regularized_Logistic_Regression.ipynb`](file:///c:/Users/harsh/OneDrive/Desktop/ML/Fertilizer_Requirement_Prediction_Regularized_Logistic_Regression.ipynb).
3. Select **Runtime > Run all** (`Ctrl + F9`).
4. **Zero-Setup Execution:** The notebook automatically generates and caches the benchmark dataset in memory if no file is uploaded, meaning it **never crashes or hangs on upload prompts**!

---

## 🧠 Machine Learning Architecture & Features

```
┌────────────────────────────────┐
│   Agricultural Dataset (CSV)   │
└───────────────┬────────────────┘
                ▼
┌────────────────────────────────┐
│  Stratified Split (80% / 20%)  │ ◄── Anti-Leakage Guard
└───────────────┬────────────────┘
                ▼
┌────────────────────────────────┐
│   Modular ColumnTransformer    │
│ • Numerical: Median + Scaler   │
│ • Categorical: Mode + One-Hot  │
└───────────────┬────────────────┘
                ▼
┌────────────────────────────────────────────────────────┐
│               Regularization Tournament                │
│  1. Baseline  2. Unregularized  3. L1  4. L2  5. ENet   │
└───────────────┬────────────────────────────────────────┘
                ▼
┌────────────────────────────────┐
│ Hyperparameter Sweep (C Path)  │ ◄── 5-Fold Stratified CV
└───────────────┬────────────────┘
                ▼
┌────────────────────────────────┐
│   Diagnostic Evaluation Suite  │
│ • ROC-AUC & PR-AUC Curves      │
│ • Calibration (Brier Score)    │
│ • Dual Confusion Matrix        │
│ • Threshold Optimization (τ*)  │
└───────────────┬────────────────┘
                ▼
┌────────────────────────────────┐
│ Odds Ratios & Interpretability │
└───────────────┬────────────────┘
                ▼
┌────────────────────────────────┐
│ Interactive Colab Simulator &  │
│ Exported Production Artifacts  │
└────────────────────────────────┘
```

### Key Highlights
- **Mathematical Formulations:** Clear LaTeX mathematical derivations for Logistic Regression, Binary Cross-Entropy, Lasso ($L_1$), Ridge ($L_2$), and ElasticNet.
- **Model Tournament:** Direct empirical benchmark comparing Dummy Baseline, Unregularized Logistic, $L_1$ Lasso, $L_2$ Ridge, and ElasticNet across Accuracy, Precision, Recall, F1, ROC-AUC, and Brier Loss.
- **L1 Regularization Path:** Coefficient shrinkage visualization showing parameters dropping to exact zero as penalty strength increases.
- **Diagnostic Suite:** Dual confusion matrix (counts + normalized %), ROC Curve (AUC $\approx 0.865$), Precision-Recall Curve (AP $\approx 0.852$), and Calibration Reliability Diagram.
- **Agricultural Cost Threshold Tuning:** Adjusts classification decision threshold $\tau$ to penalize False Negatives (nutrient starvation) 3× more than False Positives.
- **Interpretability (Odds Ratios):** $OR_j = \exp(\beta_j)$ visualization mapping feature effects directly to soil chemistry.
- **Interactive Simulator:** Form sliders for real-time what-if prediction on customized soil samples.
- **Production Artifacts:** Serialized `.joblib` pipeline bundle, `model_metadata.json`, and `inference_sample.py`.
