# Standalone Inference Script for Fertilizer Requirement Prediction
import joblib
import pandas as pd

def predict_fertilizer_need(soil_record_dict, bundle_path="fertilizer_requirement_model_bundle.joblib"):
    bundle = joblib.load(bundle_path)
    pipeline = bundle["pipeline"]
    threshold = bundle.get("optimal_threshold", 0.50)
    df_sample = pd.DataFrame([soil_record_dict])
    prob = pipeline.predict_proba(df_sample)[0, 1]
    return {
        "fertilizer_required": bool(prob >= threshold),
        "probability": round(float(prob), 4),
        "threshold": threshold
    }
