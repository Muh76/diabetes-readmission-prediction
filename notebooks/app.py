import mlflow
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Diabetic Readmission ML Pipeline", version="1.0.0")

# Load model
model = None
try:
    model = mlflow.sklearn.load_model("models://diabetic_readmission_model")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"⚠️ Model loading failed: {e}")


# Pydantic model for input validation
class PatientData(BaseModel):
    num_medications: int
    time_in_hospital: int
    number_diagnoses: int
    num_procedures: int
    num_lab_procedures: int


@app.get("/")
async def root():
    return {"message": "Diabetic Readmission ML Pipeline API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict")
async def predict_readmission(patient: PatientData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # Prepare input data
        input_data = pd.DataFrame([patient.dict()])

        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = (
            model.predict_proba(input_data)[0][1]
            if hasattr(model, "predict_proba")
            else None
        )

        return {
            "readmission_risk": bool(prediction),
            "probability": float(probability) if probability is not None else None,
            "message": "High risk of readmission"
            if prediction
            else "Low risk of readmission",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(e)}"
        ) from e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
