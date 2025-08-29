# FORCE DEPLOYMENT UPDATE - V2.0 FINAL - CACHE BUSTING COMMENT
# This comment ensures Docker builds a new layer and deploys the latest code
# Last updated: 2025-01-20 20:30 - Force rebuild to fix path issues
# Build timestamp: $(date) - Ensuring latest deployment

# =============================================================================
# DIABETIC READMISSION PREDICTION API
# Production-ready FastAPI application for ML model serving
#
# DEPLOYMENT FIX: File paths corrected to match Dockerfile structure
# - feature_names.pkl: ./feature_names.pkl (current directory)
# - feature_scaler.pkl: ./feature_scaler.pkl (current directory)
# - models: ./models/ (models subdirectory)
# =============================================================================
import logging
import os
import sys
import time
from datetime import datetime

import joblib
import pandas as pd
import psutil
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

# VERSION: 2.0 - File paths fixed for Azure deployment
# DEPLOYMENT: 2025-08-20 - Critical file path fix applied

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Diabetic Readmission ML Pipeline API",
    description="Production-ready ML API for diabetic readmission prediction with comprehensive monitoring",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Add startup event handler
@app.on_event("startup")
async def startup_event():
    """Handle startup events and model loading"""
    global startup_time, models, feature_names, feature_scaler

    startup_time = datetime.now()
    logger.info("🚀 FastAPI application starting up...")

    try:
        # Load models and features
        logger.info("📦 Loading ML models and features...")

        # Load feature scaler
        if os.path.exists("feature_scaler.pkl"):
            feature_scaler = joblib.load("feature_scaler.pkl")
            logger.info("✅ Feature scaler loaded successfully")
        else:
            logger.warning("⚠️ Feature scaler not found")

        # Load feature names
        if os.path.exists("feature_names.pkl"):
            feature_names = joblib.load("feature_names.pkl")
            logger.info(f"✅ Feature names loaded: {len(feature_names)} features")
        else:
            logger.warning("⚠️ Feature names not found")

        # Load models
        model_files = {
            "logistic_regression": "models/logistic_regression.pkl",
            "xgboost": "models/xgboost.pkl",
            "lightgbm": "models/lightgbm.pkl",
            "catboost": "models/catboost.pkl",
        }

        for model_name, model_path in model_files.items():
            try:
                if os.path.exists(model_path):
                    models[model_name] = joblib.load(model_path)
                    logger.info(f"✅ {model_name} model loaded successfully")
                else:
                    logger.warning(f"⚠️ {model_name} model not found at {model_path}")
            except Exception as e:
                logger.error(f"❌ Failed to load {model_name} model: {e}")

        logger.info(
            f"🎯 Startup completed. Models loaded: {len([m for m in models.values() if m is not None])}"
        )

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise e


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models and metadata
models = {}
feature_names = []
feature_scaler = None
model_metadata = {}
startup_time = None


# Pydantic models for input validation
class PatientData(BaseModel):
    """Patient data input model with validation - matches all engineered features (16 total)"""

    # Core patient identifiers
    encounter_id: int = Field(..., description="Unique encounter identifier")
    patient_nbr: int = Field(..., description="Unique patient number")

    # Admission and discharge information
    admission_type_id: int = Field(..., ge=1, le=9, description="Type of admission")
    discharge_disposition_id: int = Field(
        ..., ge=1, le=30, description="Discharge disposition"
    )
    admission_source_id: int = Field(
        ..., ge=1, le=25, description="Source of admission"
    )

    # Hospital stay metrics
    time_in_hospital: int = Field(
        ..., ge=1, le=365, description="Time in hospital (days)"
    )
    num_lab_procedures: int = Field(
        ..., ge=0, le=1000, description="Number of lab procedures"
    )
    num_procedures: int = Field(..., ge=0, le=100, description="Number of procedures")
    num_medications: int = Field(..., ge=0, le=100, description="Number of medications")

    # Visit history
    number_outpatient: int = Field(
        ..., ge=0, le=100, description="Number of outpatient visits"
    )
    number_emergency: int = Field(
        ..., ge=0, le=100, description="Number of emergency visits"
    )
    number_inpatient: int = Field(
        ..., ge=0, le=100, description="Number of inpatient visits"
    )
    number_diagnoses: int = Field(..., ge=1, le=50, description="Number of diagnoses")

    # Engineered features
    age_midpoint: int = Field(..., ge=0, le=100, description="Age group midpoint")
    service_utilization_score: int = Field(
        ..., ge=0, le=10, description="Service utilization score"
    )
    clinical_risk_score: int = Field(
        ..., ge=0, le=10, description="Clinical risk score"
    )

    @validator("*")
    def validate_positive(cls, v):  # noqa: N805
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v


class PredictionResponse(BaseModel):
    """Standardized prediction response model"""

    patient_id: str
    timestamp: str
    readmission_risk: bool
    probability: float
    confidence_level: str
    risk_factors: list[str]
    model_used: str
    processing_time_ms: float
    message: str


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    timestamp: str
    uptime_seconds: float
    models_loaded: int
    memory_usage_mb: float
    cpu_usage_percent: float
    disk_usage_percent: float


class ModelInfo(BaseModel):
    """Model information response model"""

    model_name: str
    model_type: str
    performance_metrics: dict[str, float]
    training_date: str
    feature_count: int
    model_size_mb: float


# Dependency for request timing
async def get_request_timing():
    return {"start_time": time.time()}


def load_models():
    """Load trained models and preprocessing artifacts"""
    global models, feature_names, feature_scaler, model_metadata

    try:
        # Load feature names and scaler - use the full feature names that match the training data
        feature_names = joblib.load("feature_names.pkl")
        feature_scaler = joblib.load("feature_scaler.pkl")
        logger.info(f"✅ Loaded {len(feature_names)} feature names")

        # Load only small models (exclude large ones)
        model_files = {
            "logistic_regression": "models/logistic_regression.pkl",
            "xgboost": "models/xgboost.pkl",
            "lightgbm": "models/lightgbm.pkl",
            "catboost": "models/catboost.pkl",
        }

        for model_name, model_path in model_files.items():
            try:
                if os.path.exists(model_path):
                    model = joblib.load(model_path)
                    models[model_name] = model

                    # Get model size
                    model_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
                    logger.info(f"✅ Loaded {model_name} model ({model_size:.2f} MB)")

                    # Store metadata
                    model_metadata[model_name] = {
                        "size_mb": model_size,
                        "type": type(model).__name__,
                        "loaded_at": datetime.now().isoformat(),
                    }
                else:
                    logger.warning(f"⚠️ Model file not found: {model_path}")
            except Exception as e:
                logger.error(f"❌ Failed to load {model_name}: {str(e)}")

        logger.info(f"🎯 Successfully loaded {len(models)} models")

    except Exception as e:
        logger.error(f"❌ Critical error loading models: {str(e)}")
        raise


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        current_time = datetime.now()
        uptime = (current_time - startup_time).total_seconds() if startup_time else 0

        # System metrics
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        disk = psutil.disk_usage("/")

        return HealthResponse(
            status="healthy" if models else "degraded",
            timestamp=current_time.isoformat(),
            uptime_seconds=round(uptime, 2),
            models_loaded=len([m for m in models.values() if m is not None]),
            memory_usage_mb=round(memory.used / (1024 * 1024), 2),
            cpu_usage_percent=round(cpu_percent, 2),
            disk_usage_percent=round((disk.used / disk.total) * 100, 2),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Health check failed: {str(e)}"
        ) from e


# Feature names endpoint
@app.get("/feature-names")
async def get_feature_names():
    """Get the list of feature names expected by the model"""
    try:
        if not feature_names:
            raise HTTPException(
                status_code=500,
                detail="Feature names not loaded. Please check if models are properly initialized.",
            )

        return {
            "feature_count": len(feature_names),
            "features": feature_names,
            "description": "List of engineered features expected by the ML model",
        }
    except Exception as e:
        logger.error(f"Failed to get feature names: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get feature names: {str(e)}"
        ) from e


# Model information endpoint
@app.get("/models", response_model=list[ModelInfo])
async def get_models_info():
    """Get information about all loaded models"""
    try:
        model_info_list = []

        for model_name, model in models.items():
            if model is not None:
                # Get model type
                model_type = type(model).__name__

                # Get performance metrics from training results
                performance_metrics = {}
                try:
                    training_results_path = os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "models",
                        "training_results.pkl",
                    )
                    if os.path.exists(training_results_path):
                        training_results = joblib.load(training_results_path)
                        if model_name in training_results:
                            performance_metrics = training_results[model_name]
                except Exception:
                    pass

                model_info_list.append(
                    ModelInfo(
                        model_name=model_name,
                        model_type=model_type,
                        performance_metrics=performance_metrics,
                        training_date=model_metadata[model_name].get(
                            "loaded_at", "Unknown"
                        ),
                        feature_count=len(feature_names) if feature_names else 0,
                        model_size_mb=model_metadata[model_name].get("size_mb", 0),
                    )
                )

        return model_info_list
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get model info: {str(e)}"
        ) from e


# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict_readmission(
    patient: PatientData,
    model_name: str = "xgboost",
    timing: dict = Depends(get_request_timing),
):
    """Predict diabetic readmission risk for a patient"""
    start_time = timing["start_time"]

    try:
        # Validate model selection
        if model_name not in models or models[model_name] is None:
            available_models = list(models.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Model '{model_name}' not available. Available models: {available_models}",
            )

        # Prepare input data - ensure correct feature order
        patient_dict = patient.dict()
        input_data = pd.DataFrame([patient_dict])

        # Ensure features are in the correct order as expected by the model
        if feature_names:
            # Check if we have all required features
            missing_features = [f for f in feature_names if f not in input_data.columns]
            if missing_features:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required features: {missing_features}",
                )

            # Select only the features that the model expects
            input_data = input_data[feature_names]
            logger.info(f"✅ Selected {len(input_data.columns)} features for prediction")

        # Validate feature count
        if len(input_data.columns) != len(feature_names):
            logger.warning(
                f"Feature count mismatch: expected {len(feature_names)}, got {len(input_data.columns)}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Feature count mismatch: expected {len(feature_names)}, got {len(input_data.columns)}",
            )

        # Scale features if scaler is available
        if feature_scaler is not None:
            input_data = feature_scaler.transform(input_data)
            logger.info(f"✅ Features scaled using {type(feature_scaler).__name__}")

        # Make prediction
        model = models[model_name]
        prediction = model.predict(input_data)[0]

        # Get probability if available
        probability = None
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_data)[0][1]
        elif hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_data)[0][1]

        # Determine confidence level
        if probability is not None:
            if probability > 0.8 or probability < 0.2:
                confidence_level = "High"
            elif probability > 0.6 or probability < 0.4:
                confidence_level = "Medium"
            else:
                confidence_level = "Low"
        else:
            confidence_level = "Unknown"

        # Identify risk factors based on engineered features
        risk_factors = []
        if patient.num_medications > 10:
            risk_factors.append("High medication count")
        if patient.time_in_hospital > 14:
            risk_factors.append("Extended hospital stay")
        if patient.number_diagnoses > 5:
            risk_factors.append("Multiple diagnoses")
        if patient.clinical_risk_score > 7:
            risk_factors.append("High clinical risk score")
        if patient.service_utilization_score > 7:
            risk_factors.append("High service utilization")
        if patient.age_midpoint > 70:
            risk_factors.append("Advanced age group")

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Generate response
        response = PredictionResponse(
            patient_id=f"PAT_{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            readmission_risk=bool(prediction),
            probability=float(probability) if probability is not None else 0.0,
            confidence_level=confidence_level,
            risk_factors=risk_factors,
            model_used=model_name,
            processing_time_ms=round(processing_time, 2),
            message="High risk of readmission"
            if prediction
            else "Low risk of readmission",
        )

        logger.info(
            f"✅ Prediction completed for patient {response.patient_id} using {model_name}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(e)}"
        ) from e


# Batch prediction endpoint
@app.post("/predict/batch")
async def predict_batch(patients: list[PatientData], model_name: str = "xgboost"):
    """Predict readmission risk for multiple patients"""
    try:
        if model_name not in models or models[model_name] is None:
            available_models = list(models.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Model '{model_name}' not available. Available models: {available_models}",
            )

        results = []
        for i, patient in enumerate(patients):
            try:
                # Create single prediction request
                single_result = await predict_readmission(patient, model_name)
                results.append(single_result.dict())
            except Exception as e:
                results.append(
                    {
                        "patient_id": f"PAT_BATCH_{i}",
                        "error": str(e),
                        "status": "failed",
                    }
                )

        return {
            "batch_id": f"BATCH_{int(time.time())}",
            "total_patients": len(patients),
            "successful_predictions": len([r for r in results if "error" not in r]),
            "failed_predictions": len([r for r in results if "error" in r]),
            "results": results,
        }

    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Batch prediction failed: {str(e)}"
        ) from e


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint with basic information"""
    return {
        "message": "Diabetic Readmission ML Pipeline API",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
        "models": "/models",
        "timestamp": datetime.now().isoformat(),
        "deployment": "Railway Production",
    }


# Simple health check for Railway deployment
@app.get("/health")
async def simple_health_check():
    """Simple health check endpoint for Railway deployment"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Diabetes Readmission API",
        "version": "2.0.0",
    }


# Readiness check for Railway
@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint for Railway deployment"""
    try:
        # Check if basic components are loaded
        basic_ready = (
            feature_scaler is not None and len(feature_names) > 0 and len(models) > 0
        )

        return {
            "ready": basic_ready,
            "timestamp": datetime.now().isoformat(),
            "components": {
                "feature_scaler": feature_scaler is not None,
                "feature_names": len(feature_names) > 0,
                "models": len(models) > 0,
            },
        }
    except Exception as e:
        return {
            "ready": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for better error responses"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI server...")
    logger.info("✅ Health endpoint available at /health")
    logger.info("✅ Root endpoint available at /")
    logger.info("✅ API docs available at /docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", access_log=True)
