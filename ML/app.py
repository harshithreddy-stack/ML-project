"""
AgriFertilizer AI - FastAPI Web Application
Machine Learning Driven Agricultural Fertilizer Requirement Prediction System
Authors: Sai Snehith (2520090149) & Harshith Reddy (2520090114)
Department: CSIT
"""

import os
from typing import Optional, Dict, Any, List
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLE_PATH = os.path.join(BASE_DIR, "fertilizer_requirement_model_bundle.joblib")
DATASET_PATH = os.path.join(BASE_DIR, "fertilizer_requirement_dataset.csv")

app = FastAPI(
    title="AgriFertilizer AI - Fertilizer Advisory System",
    description="Precision Agricultural AI for Fertilizer Requirement Prediction using Regularized Logistic Regression",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model Bundle
model_bundle: Dict[str, Any] = {}
try:
    if os.path.exists(BUNDLE_PATH):
        model_bundle = joblib.load(BUNDLE_PATH)
        print("[OK] Successfully loaded fertilizer requirement model bundle.")
    else:
        print(f"[Warning] Model bundle not found at {BUNDLE_PATH}")
except Exception as e:
    print(f"[Error] Error loading model bundle: {e}")

class SoilPredictionRequest(BaseModel):
    Nitrogen: float = Field(..., ge=0.0, le=200.0, description="Nitrogen content in kg/ha")
    Phosphorus: float = Field(..., ge=0.0, le=200.0, description="Phosphorus content in kg/ha")
    Potassium: float = Field(..., ge=0.0, le=200.0, description="Potassium content in kg/ha")
    pH: float = Field(..., ge=3.0, le=10.0, description="Soil pH value")
    Soil_Moisture: float = Field(..., ge=0.0, le=100.0, description="Soil moisture percentage")
    Temperature: float = Field(..., ge=-10.0, le=60.0, description="Ambient temperature in °C")
    Humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity percentage")
    Rainfall: float = Field(..., ge=0.0, le=600.0, description="Rainfall in mm")
    Soil_Type: str = Field(..., description="Soil type: Black, Clayey, Red, Loamy, Laterite, Sandy")
    Crop_Type: str = Field(..., description="Crop type: Rice, Wheat, Maize, Cotton, Sugarcane, Pulses, Barley, Soybean, Groundnut, Mustard")

PRESETS = [
    {
        "id": "low_n_rice",
        "title": "🌾 Rice Paddy - Severe Nitrogen Deficiency",
        "description": "Clayey soil with depleted nitrogen (N=14 kg/ha) during tillering stage.",
        "badge": "Fertilizer Required",
        "expected_fertilizer": "Urea",
        "data": {
            "Nitrogen": 14.0,
            "Phosphorus": 48.0,
            "Potassium": 52.0,
            "pH": 6.8,
            "Soil_Moisture": 68.0,
            "Temperature": 28.5,
            "Humidity": 78.0,
            "Rainfall": 175.0,
            "Soil_Type": "Clayey",
            "Crop_Type": "Rice"
        }
    },
    {
        "id": "low_p_groundnut",
        "title": "🥜 Groundnut - Phosphorus Deficiency",
        "description": "Red soil with critically low phosphorus (P=9 kg/ha) impeding root nodule formation.",
        "badge": "Fertilizer Required",
        "expected_fertilizer": "DAP",
        "data": {
            "Nitrogen": 58.0,
            "Phosphorus": 9.2,
            "Potassium": 46.0,
            "pH": 6.3,
            "Soil_Moisture": 32.0,
            "Temperature": 31.0,
            "Humidity": 58.0,
            "Rainfall": 95.0,
            "Soil_Type": "Red",
            "Crop_Type": "Groundnut"
        }
    },
    {
        "id": "low_k_sugarcane",
        "title": "🎋 Sugarcane - Potassium Depletion",
        "description": "Heavy feeder crop in Loamy soil lacking potassium (K=12 kg/ha) for sucrose synthesis.",
        "badge": "Fertilizer Required",
        "expected_fertilizer": "MOP",
        "data": {
            "Nitrogen": 72.0,
            "Phosphorus": 45.0,
            "Potassium": 12.0,
            "pH": 7.1,
            "Soil_Moisture": 55.0,
            "Temperature": 32.0,
            "Humidity": 65.0,
            "Rainfall": 140.0,
            "Soil_Type": "Loamy",
            "Crop_Type": "Sugarcane"
        }
    },
    {
        "id": "optimal_wheat",
        "title": "🌾 Fertile Wheat Field - Optimal Nutrients",
        "description": "Balanced Black soil with rich N-P-K reserves; no chemical supplementation required.",
        "badge": "Nutrients Adequate",
        "expected_fertilizer": "None",
        "data": {
            "Nitrogen": 82.0,
            "Phosphorus": 56.0,
            "Potassium": 62.0,
            "pH": 7.2,
            "Soil_Moisture": 42.0,
            "Temperature": 22.0,
            "Humidity": 50.0,
            "Rainfall": 80.0,
            "Soil_Type": "Black",
            "Crop_Type": "Wheat"
        }
    },
    {
        "id": "multi_deficient_maize",
        "title": "🌽 Maize - Multi-Nutrient Deficit",
        "description": "Laterite soil with severe N, P and K depletion needing comprehensive fertilization.",
        "badge": "Fertilizer Required",
        "expected_fertilizer": "NPK Complex (17-17-17)",
        "data": {
            "Nitrogen": 18.0,
            "Phosphorus": 14.0,
            "Potassium": 16.0,
            "pH": 5.9,
            "Soil_Moisture": 28.0,
            "Temperature": 29.0,
            "Humidity": 62.0,
            "Rainfall": 110.0,
            "Soil_Type": "Laterite",
            "Crop_Type": "Maize"
        }
    },
    {
        "id": "sandy_cotton",
        "title": "🌱 Sandy Soil Cotton - Marginal Fertility",
        "description": "Fast-draining sandy soil with moderate moisture and mild nitrogen deficit.",
        "badge": "Fertilizer Required",
        "expected_fertilizer": "Urea",
        "data": {
            "Nitrogen": 28.0,
            "Phosphorus": 38.0,
            "Potassium": 41.0,
            "pH": 6.6,
            "Soil_Moisture": 24.0,
            "Temperature": 33.5,
            "Humidity": 48.0,
            "Rainfall": 70.0,
            "Soil_Type": "Sandy",
            "Crop_Type": "Cotton"
        }
    }
]

def analyze_soil_chemistry(n: float, p: float, k: float, ph: float, moisture: float, crop: str):
    """
    Evaluates individual macro-nutrients against agronomic sufficiency thresholds
    and determines specific fertilizer dosage requirements.
    """
    # Benchmarks (kg/ha)
    n_status = "Optimal"
    if n < 30:
        n_status = "Severely Deficient"
    elif n < 50:
        n_status = "Low"
    elif n > 110:
        n_status = "High"

    p_status = "Optimal"
    if p < 18:
        p_status = "Severely Deficient"
    elif p < 30:
        p_status = "Low"
    elif p > 80:
        p_status = "High"

    k_status = "Optimal"
    if k < 20:
        k_status = "Severely Deficient"
    elif k < 35:
        k_status = "Low"
    elif k > 85:
        k_status = "High"

    # pH status
    if ph < 5.5:
        ph_label = "Strongly Acidic"
        ph_advice = "Nutrient availability (P, K) may be reduced. Consider agricultural lime (CaCO3) application to raise soil pH."
    elif ph < 6.5:
        ph_label = "Slightly Acidic"
        ph_advice = "Good condition for most cereals and pulses with balanced micronutrient absorption."
    elif ph <= 7.5:
        ph_label = "Neutral (Optimal)"
        ph_advice = "Ideal physiological range for root uptake and microbial nutrient cycling."
    elif ph <= 8.5:
        ph_label = "Moderately Alkaline"
        ph_advice = "Phosphorus fixation risk. Consider gypsum or organic composting amendments to moderate alkalinity."
    else:
        ph_label = "Strongly Alkaline"
        ph_advice = "High saline/alkaline condition. Soil conditioning required to prevent micronutrient lock-out."

    return {
        "nitrogen": {"value": n, "status": n_status, "benchmark_target": "50 - 100 kg/ha", "unit": "kg/ha"},
        "phosphorus": {"value": p, "status": p_status, "benchmark_target": "30 - 65 kg/ha", "unit": "kg/ha"},
        "potassium": {"value": k, "status": k_status, "benchmark_target": "35 - 75 kg/ha", "unit": "kg/ha"},
        "ph": {"value": ph, "status": ph_label, "advice": ph_advice},
        "moisture": {"value": moisture, "status": "Low" if moisture < 30 else ("High" if moisture > 70 else "Adequate")}
    }

def determine_fertilizer_prescription(n: float, p: float, k: float, crop: str) -> Dict[str, str]:
    """
    Identifies specific fertilizer product (Urea, DAP, MOP, or NPK Complex)
    matching agronomic deficiency patterns.
    """
    deficits = []
    if n < 45:
        deficits.append(("N", 45 - n))
    if p < 28:
        deficits.append(("P", (28 - p) * 1.5))  # P deficit weighted
    if k < 32:
        deficits.append(("K", (32 - k) * 1.3))  # K deficit weighted

    if not deficits:
        return {
            "fertilizer": "None Required",
            "formula": "Natural Soil Reserves Sufficient",
            "application": "Maintain organic mulch and standard crop rotation to preserve soil structure."
        }

    # If all three are deficient
    if len(deficits) >= 3:
        return {
            "fertilizer": "NPK Complex (17-17-17)",
            "formula": "Balanced Nitrogen-Phosphorus-Potassium Complex",
            "application": "Apply basal dressing of balanced NPK complex (100-120 kg/ha) at sowing or early vegetative phase."
        }

    # Sort by greatest relative deficit
    deficits.sort(key=lambda x: x[1], reverse=True)
    primary = deficits[0][0]

    if primary == "P":
        return {
            "fertilizer": "DAP (Di-Ammonium Phosphate)",
            "formula": "18% N + 46% P2O5",
            "application": "Apply 75-100 kg/ha at root depth during land preparation or basal planting for stimulated root growth."
        }
    elif primary == "K":
        return {
            "fertilizer": "MOP (Muriate of Potash)",
            "formula": "0% N + 0% P + 60% K2O",
            "application": "Broadcast 40-60 kg/ha prior to flowering/tuber filling to strengthen stalk resistance and drought tolerance."
        }
    else:  # Primary N
        return {
            "fertilizer": "Urea",
            "formula": "46% Nitrogen (46-0-0)",
            "application": "Split apply 60-90 kg/ha in 2-3 vegetative phases under moist soil conditions to prevent volatilization loss."
        }

@app.get("/api/metadata")
def get_metadata():
    if not model_bundle:
        raise HTTPException(status_code=500, detail="Model bundle not loaded")
    
    meta = model_bundle.get("metadata", {})
    return {
        "project": meta.get("project", "Fertilizer Requirement Prediction"),
        "authors": meta.get("authors", ["Sai Snehith (2520090149)", "Harshith Reddy (2520090114)"]),
        "department": meta.get("department", "CSIT"),
        "algorithm": "L1 Lasso Regularized Logistic Regression (liblinear solver)",
        "optimal_threshold": model_bundle.get("optimal_threshold", 0.52),
        "test_f1_score": meta.get("test_f1_score", 0.8102),
        "test_roc_auc": meta.get("test_roc_auc", 0.8787),
        "features": model_bundle.get("feature_names", []),
        "status": "Production Ready"
    }

@app.get("/api/presets")
def get_presets():
    return PRESETS

@app.post("/api/predict")
def predict_fertilizer(req: SoilPredictionRequest):
    if not model_bundle or "pipeline" not in model_bundle:
        raise HTTPException(status_code=500, detail="Inference pipeline unavailable")

    pipeline = model_bundle["pipeline"]
    threshold = float(model_bundle.get("optimal_threshold", 0.52))

    record = {
        "Nitrogen": req.Nitrogen,
        "Phosphorus": req.Phosphorus,
        "Potassium": req.Potassium,
        "pH": req.pH,
        "Soil_Moisture": req.Soil_Moisture,
        "Temperature": req.Temperature,
        "Humidity": req.Humidity,
        "Rainfall": req.Rainfall,
        "Soil_Type": req.Soil_Type,
        "Crop_Type": req.Crop_Type
    }

    df_sample = pd.DataFrame([record])
    try:
        prob = float(pipeline.predict_proba(df_sample)[0, 1])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

    fertilizer_needed = bool(prob >= threshold)
    
    # Assess requirement severity / risk
    if prob < 0.25:
        urgency = "Minimal"
        status_color = "success"
    elif prob < threshold:
        urgency = "Low"
        status_color = "optimal"
    elif prob < 0.75:
        urgency = "High"
        status_color = "warning"
    else:
        urgency = "Critical"
        status_color = "danger"

    nutrient_eval = analyze_soil_chemistry(
        req.Nitrogen, req.Phosphorus, req.Potassium,
        req.pH, req.Soil_Moisture, req.Crop_Type
    )

    if fertilizer_needed:
        prescription = determine_fertilizer_prescription(
            req.Nitrogen, req.Phosphorus, req.Potassium, req.Crop_Type
        )
    else:
        prescription = {
            "fertilizer": "No Chemical Fertilizer Needed",
            "formula": "Soil Nutrients Within Optimal Range",
            "application": "Soil health is well-balanced for target yield. Maintain regular crop scouting and organic mulching."
        }

    return {
        "fertilizer_required": fertilizer_needed,
        "probability": round(prob, 4),
        "probability_percentage": round(prob * 100, 1),
        "threshold": threshold,
        "threshold_percentage": round(threshold * 100, 1),
        "urgency": urgency,
        "status_color": status_color,
        "prescription": prescription,
        "nutrient_analysis": nutrient_eval,
        "input_summary": record
    }

# Mount static folder
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "AgriFertilizer AI backend is active. Place index.html in the static directory."}
