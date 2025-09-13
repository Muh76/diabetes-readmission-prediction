from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import joblib
import os
import logging
from datetime import datetime
import uvicorn
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and scaler
model = None
scaler = None
feature_names = None
model_metadata = {}

# Pydantic models
class PatientData(BaseModel):
    """Patient data model for prediction requests"""
    time_in_hospital: int = Field(..., ge=1, le=14)
    num_medications: int = Field(..., ge=0, le=81)
    number_diagnoses: int = Field(..., ge=1, le=16)
    age: str = Field(...)
    gender: Optional[str] = Field("Unknown")
    race: Optional[str] = Field("Unknown")
    admission_type_id: Optional[int] = Field(1)
    discharge_disposition_id: Optional[int] = Field(1)
    admission_source_id: Optional[int] = Field(7)
    payer_code: Optional[str] = Field("Unknown")
    medical_specialty: Optional[str] = Field("Unknown")
    num_lab_procedures: Optional[int] = Field(0, ge=0, le=100)
    num_procedures: Optional[int] = Field(0, ge=0, le=20)
    number_outpatient: Optional[int] = Field(0, ge=0, le=50)
    number_emergency: Optional[int] = Field(0, ge=0, le=50)
    number_inpatient: Optional[int] = Field(0, ge=0, le=50)
    diag_1: Optional[str] = Field("Unknown")
    diag_2: Optional[str] = Field("Unknown")
    diag_3: Optional[str] = Field("Unknown")
    max_glu_serum: Optional[str] = Field("Normal")
    A1Cresult: Optional[str] = Field("Normal")
    metformin: Optional[str] = Field("No")
    repaglinide: Optional[str] = Field("No")
    nateglinide: Optional[str] = Field("No")
    chlorpropamide: Optional[str] = Field("No")
    glimepiride: Optional[str] = Field("No")
    acetohexamide: Optional[str] = Field("No")
    glipizide: Optional[str] = Field("No")
    glyburide: Optional[str] = Field("No")
    tolbutamide: Optional[str] = Field("No")
    pioglitazone: Optional[str] = Field("No")
    rosiglitazone: Optional[str] = Field("No")
    acarbose: Optional[str] = Field("No")
    miglitol: Optional[str] = Field("No")
    troglitazone: Optional[str] = Field("No")
    tolazamide: Optional[str] = Field("No")
    examide: Optional[str] = Field("No")
    citoglipton: Optional[str] = Field("No")
    insulin: Optional[str] = Field("No")
    glyburide_metformin: Optional[str] = Field("No")
    glipizide_metformin: Optional[str] = Field("No")
    glimepiride_pioglitazone: Optional[str] = Field("No")
    metformin_rosiglitazone: Optional[str] = Field("No")
    metformin_pioglitazone: Optional[str] = Field("No")
    change: Optional[str] = Field("No")
    diabetes_med: Optional[str] = Field("No")

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    prediction: int = Field(..., description="Prediction (0=No Readmission, 1=Readmission)")
    probability: float = Field(..., ge=0.0, le=1.0, description="Prediction probability")
    risk_level: str = Field(..., description="Risk level (Low/Medium/High)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence")
    model_version: str = Field(..., description="Model version")
    timestamp: str = Field(..., description="Prediction timestamp")
    features_used: List[str] = Field(..., description="Features used for prediction")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str
    uptime: float
    model_loaded: bool
    model_performance: Dict[str, float]

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting up Diabetes Readmission Prediction API...")
    await load_model()
    yield
    # Shutdown
    logger.info("Shutting down API...")

# Create FastAPI app
app = FastAPI(
    title="Diabetes Readmission Prediction API",
    description="Machine Learning API for predicting 30-day readmission risk in diabetic patients",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model loading function
async def load_model():
    """Load the trained model and scaler"""
    global model, scaler, feature_names, model_metadata
    
    try:
        # Load model
        model_path = os.getenv("MODEL_PATH", "./models/lightgbm_optimized.pkl")
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
        else:
            logger.error(f"Model file not found: {model_path}")
            return False
            
        # Load scaler
        scaler_path = os.getenv("SCALER_PATH", "./models/feature_scaler.pkl")
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")
            
        # Load feature names
        feature_names_path = os.getenv("FEATURE_NAMES_PATH", "./models/feature_names.pkl")
        if os.path.exists(feature_names_path):
            feature_names = joblib.load(feature_names_path)
            logger.info(f"Feature names loaded from {feature_names_path}")
            
        # Set model metadata
        model_metadata = {
            "model_type": "LightGBM",
            "training_date": "2024-01-01",
            "performance": {
                "roc_auc": 0.6745,
                "accuracy": 0.6599,
                "precision": 0.1735,
                "recall": 0.5811,
                "f1_score": 0.2673
            },
            "features_count": len(feature_names) if feature_names else 0
        }
        
        logger.info("Model loading completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

# Dependency to check if model is loaded
async def get_model():
    """Dependency to ensure model is loaded"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return model

# Feature preprocessing function
def preprocess_features(patient_data: PatientData) -> np.ndarray:
    """Preprocess patient data for prediction"""
    try:
        # Convert to DataFrame
        data_dict = patient_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Handle categorical variables
        categorical_features = [
            'gender', 'race', 'payer_code', 'medical_specialty',
            'diag_1', 'diag_2', 'diag_3', 'max_glu_serum', 'A1Cresult',
            'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
            'glimepiride', 'acetohexamide', 'glipizide', 'glyburide',
            'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose',
            'miglitol', 'troglitazone', 'tolazamide', 'examide',
            'citoglipton', 'insulin', 'glyburide_metformin',
            'glipizide_metformin', 'glimepiride_pioglitazone',
            'metformin_rosiglitazone', 'metformin_pioglitazone',
            'change', 'diabetes_med', 'age'
        ]
        
        # One-hot encode categorical variables
        for col in categorical_features:
            if col in df.columns:
                df = pd.get_dummies(df, columns=[col], prefix=[col])
        
        # Ensure all expected features are present
        if feature_names is not None:
            missing_features = [feature for feature in feature_names if feature not in df.columns]
            if missing_features:
                # Create a DataFrame with missing features set to 0
                missing_df = pd.DataFrame(0, index=df.index, columns=missing_features)
                # Concatenate instead of adding one by one to avoid fragmentation
                df = pd.concat([df, missing_df], axis=1)
        
        # Select only the features used in training
        if feature_names is not None:
            df = df[feature_names]
        
        # Convert to numpy array
        features = df.values.astype(np.float32)
        
        # Scale features if scaler is available
        if scaler is not None:
            features = scaler.transform(features)
            
        return features
        
    except Exception as e:
        logger.error(f"Error preprocessing features: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Feature preprocessing failed: {str(e)}")

# Risk level determination
def determine_risk_level(probability: float) -> str:
    """Determine risk level based on probability"""
    if probability < 0.3:
        return "Low"
    elif probability < 0.7:
        return "Medium"
    else:
        return "High"

# Confidence calculation
def calculate_confidence(probability: float) -> float:
    """Calculate model confidence based on probability"""
    return abs(probability - 0.5) * 2

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Diabetes Readmission Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        version="1.0.0",
        uptime=0.0,
        model_loaded=model is not None,
        model_performance=model_metadata.get("performance", {})
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_readmission(
    patient: PatientData,
    background_tasks: BackgroundTasks,
    model_dep: Any = Depends(get_model)
):
    """Predict 30-day readmission risk for a single patient"""
    try:
        # Preprocess features
        features = preprocess_features(patient)
        
        # Make prediction
        probability = model.predict_proba(features)[0][1]
        prediction = int(probability > 0.5)
        
        # Determine risk level and confidence
        risk_level = determine_risk_level(probability)
        confidence = calculate_confidence(probability)
        
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            risk_level=risk_level,
            confidence=confidence,
            model_version="1.0.0",
            timestamp=datetime.utcnow().isoformat() + "Z",
            features_used=list(feature_names) if feature_names is not None else []
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/model/info")
async def get_model_info():
    """Get information about the deployed model"""
    return {
        "model_version": "1.0.0",
        "training_date": model_metadata.get("training_date", "Unknown"),
        "performance_metrics": model_metadata.get("performance", {}),
        "feature_count": model_metadata.get("features_count", 0),
        "model_type": model_metadata.get("model_type", "Unknown"),
        "feature_names": list(feature_names) if feature_names is not None else []
    }

# Main function for running the app
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development",
        log_level="info"
    )