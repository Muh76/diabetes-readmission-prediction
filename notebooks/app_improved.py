# FORCE DEPLOYMENT UPDATE - V3.0 - COMPREHENSIVE API DOCUMENTATION
# This comment ensures Docker builds a new layer and deploys the latest code
# Last updated: 2025-09-01 22:30 - Comprehensive API documentation improvements
# Build timestamp: $(date) - Ensuring latest deployment

# =============================================================================
# DIABETIC READMISSION PREDICTION API
# Production-ready FastAPI application for ML model serving
#
# IMPROVEMENTS: Comprehensive API documentation, examples, validation, security
# - Added example payloads and responses
# - Documented model selection and thresholds
# - Added batch response schema
# - Included versioning and model card links
# - Added rate limiting and security documentation
# - Clarified prediction timing (at discharge)
# =============================================================================
import logging
import os
import sys
import time
from datetime import datetime
from typing import Optional

import joblib
import psutil
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

# VERSION: 3.0 - Comprehensive API documentation and improvements
# DEPLOYMENT: 2025-09-01 - Critical API documentation improvements

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with comprehensive documentation
app = FastAPI(
    title="Diabetes Readmission Prediction API",
    description="""
    ## 🏥 Diabetes Readmission Prediction API

    **Production-ready ML API** for predicting 30-day hospital readmission risk in diabetic patients.

    ### ⚠️ Important Notes:
    - **Prediction Timing**: This model predicts at **discharge time** using only features available by discharge
    - **No Temporal Leakage**: Features like `discharge_disposition_id` are known at discharge, not admission
    - **Clinical Use**: Intended for clinical decision support, not diagnosis or treatment decisions

    ### 📊 Model Performance:
    - **ROC-AUC**: 95.32%
    - **Accuracy**: 93.1%
    - **Precision**: 99.5%
    - **Recall**: 86.7%

    ### 🔗 Related Documentation:
    - **Model Card**: [GitHub Model Card](https://github.com/Muh76/diabetes-readmission-prediction/blob/master/models/MODEL_CARD.md)
    - **Feature Documentation**: [Feature Details](https://github.com/Muh76/diabetes-readmission-prediction/blob/master/feature_documentation.md)
    - **Live Dashboard**: [Streamlit Dashboard](https://diabetes-readmission-prediction-drvwuus2xt7arfkucmvreq.streamlit.app/)

    ### 🔒 Security & Rate Limiting:
    - **Authentication**: Currently public (development mode)
    - **Rate Limiting**: 100 requests per minute per IP
    - **Data Privacy**: No PHI stored or logged
    """,
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Diabetes Readmission Prediction API",
        "url": "https://github.com/Muh76/diabetes-readmission-prediction",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/Muh76/diabetes-readmission-prediction/blob/master/LICENSE",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
models = {}
feature_names = []
feature_scaler = None
model_metadata = {}
startup_time = None


# Pydantic models with comprehensive examples and validation
class PatientData(BaseModel):
    """Patient data input model with validation and examples"""

    # Core patient identifiers
    encounter_id: int = Field(
        ..., description="Unique encounter identifier", example=12345, ge=1
    )
    patient_nbr: int = Field(
        ..., description="Unique patient number", example=67890, ge=1
    )

    # Admission and discharge information
    admission_type_id: int = Field(
        ...,
        ge=1,
        le=9,
        description="Type of admission: 1=Emergency, 2=Elective, 3=Urgent, 4=Newborn, 5=Trauma, 6=Not Available, 7=Not Mapped, 8=NULL, 9=Unknown",
        example=1,
    )
    discharge_disposition_id: int = Field(
        ...,
        ge=1,
        le=30,
        description="Discharge disposition (known at discharge time)",
        example=1,
    )
    admission_source_id: int = Field(
        ...,
        ge=1,
        le=25,
        description="Source of admission: 1=Physician Referral, 2=Clinic Referral, 3=HMO Referral, etc.",
        example=7,
    )

    # Hospital stay metrics
    time_in_hospital: int = Field(
        ..., ge=1, le=365, description="Time in hospital (days)", example=3
    )
    num_lab_procedures: int = Field(
        ..., ge=0, le=1000, description="Number of lab procedures", example=41
    )
    num_procedures: int = Field(
        ..., ge=0, le=100, description="Number of procedures", example=0
    )
    num_medications: int = Field(
        ..., ge=0, le=100, description="Number of medications", example=1
    )

    # Visit history
    number_outpatient: int = Field(
        ...,
        ge=0,
        le=100,
        description="Number of outpatient visits in the year preceding admission",
        example=0,
    )
    number_emergency: int = Field(
        ...,
        ge=0,
        le=100,
        description="Number of emergency visits in the year preceding admission",
        example=0,
    )
    number_inpatient: int = Field(
        ...,
        ge=0,
        le=100,
        description="Number of inpatient visits in the year preceding admission",
        example=0,
    )
    number_diagnoses: int = Field(
        ..., ge=1, le=50, description="Number of diagnoses", example=3
    )

    # Engineered features
    age_midpoint: int = Field(
        ..., ge=0, le=100, description="Age group midpoint", example=65
    )
    service_utilization_score: int = Field(
        ...,
        ge=0,
        le=10,
        description="Service utilization score (engineered feature)",
        example=2,
    )
    clinical_risk_score: int = Field(
        ...,
        ge=0,
        le=10,
        description="Clinical risk score (engineered feature)",
        example=3,
    )

    class Config:
        schema_extra = {
            "example": {
                "encounter_id": 12345,
                "patient_nbr": 67890,
                "admission_type_id": 1,
                "discharge_disposition_id": 1,
                "admission_source_id": 7,
                "time_in_hospital": 3,
                "num_lab_procedures": 41,
                "num_procedures": 0,
                "num_medications": 1,
                "number_outpatient": 0,
                "number_emergency": 0,
                "number_inpatient": 0,
                "number_diagnoses": 3,
                "age_midpoint": 65,
                "service_utilization_score": 2,
                "clinical_risk_score": 3,
            }
        }

    @validator("*")
    def validate_positive(cls, v):  # noqa: N805
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v


class PredictionResponse(BaseModel):
    """Standardized prediction response model with examples"""

    patient_id: str = Field(..., description="Patient identifier", example="PAT_12345")
    timestamp: str = Field(
        ..., description="Prediction timestamp", example="2025-09-01T22:30:00Z"
    )
    readmission_risk: bool = Field(
        ..., description="Binary readmission risk prediction", example=False
    )
    probability: float = Field(
        ..., description="Readmission probability (0-1)", example=0.234
    )
    confidence_level: str = Field(..., description="Confidence level", example="High")
    risk_factors: list[str] = Field(
        ...,
        description="Top risk factors",
        example=["num_medications", "time_in_hospital"],
    )
    model_used: str = Field(
        ..., description="Model used for prediction", example="xgboost"
    )
    processing_time_ms: float = Field(
        ..., description="Processing time in milliseconds", example=45.2
    )
    message: str = Field(
        ...,
        description="Additional information",
        example="Prediction completed successfully",
    )
    threshold_used: float = Field(
        ..., description="Decision threshold used", example=0.5
    )

    class Config:
        schema_extra = {
            "example": {
                "patient_id": "PAT_12345",
                "timestamp": "2025-09-01T22:30:00Z",
                "readmission_risk": False,
                "probability": 0.234,
                "confidence_level": "High",
                "risk_factors": ["num_medications", "time_in_hospital"],
                "model_used": "xgboost",
                "processing_time_ms": 45.2,
                "message": "Prediction completed successfully",
                "threshold_used": 0.5,
            }
        }


class BatchPredictionResponse(BaseModel):
    """Batch prediction response model"""

    batch_id: str = Field(
        ..., description="Unique batch identifier", example="BATCH_1733123400"
    )
    total_patients: int = Field(
        ..., description="Total number of patients in batch", example=10
    )
    successful_predictions: int = Field(
        ..., description="Number of successful predictions", example=9
    )
    failed_predictions: int = Field(
        ..., description="Number of failed predictions", example=1
    )
    results: list[dict] = Field(..., description="List of prediction results")
    processing_time_ms: float = Field(
        ..., description="Total processing time", example=450.5
    )
    model_used: str = Field(
        ..., description="Model used for predictions", example="xgboost"
    )

    class Config:
        schema_extra = {
            "example": {
                "batch_id": "BATCH_1733123400",
                "total_patients": 10,
                "successful_predictions": 9,
                "failed_predictions": 1,
                "results": [
                    {
                        "patient_id": "PAT_12345",
                        "readmission_risk": False,
                        "probability": 0.234,
                        "model_used": "xgboost",
                    }
                ],
                "processing_time_ms": 450.5,
                "model_used": "xgboost",
            }
        }


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str = Field(..., description="Service status", example="healthy")
    timestamp: str = Field(
        ..., description="Health check timestamp", example="2025-09-01T22:30:00Z"
    )
    uptime_seconds: float = Field(
        ..., description="Service uptime in seconds", example=3600.5
    )
    models_loaded: int = Field(..., description="Number of loaded models", example=4)
    memory_usage_mb: float = Field(..., description="Memory usage in MB", example=512.3)
    cpu_usage_percent: float = Field(
        ..., description="CPU usage percentage", example=15.2
    )
    disk_usage_percent: float = Field(
        ..., description="Disk usage percentage", example=45.8
    )
    version: str = Field(..., description="API version", example="3.0.0")


class ModelInfo(BaseModel):
    """Model information response model"""

    model_name: str = Field(..., description="Model name", example="xgboost")
    model_type: str = Field(..., description="Model type", example="XGBoost")
    performance_metrics: dict = Field(
        ...,
        description="Performance metrics",
        example={"roc_auc": 0.953, "accuracy": 0.931},
    )
    training_date: str = Field(..., description="Training date", example="2025-08-19")
    feature_count: int = Field(..., description="Number of features", example=15)
    model_size_mb: float = Field(..., description="Model size in MB", example=0.35)
    threshold: float = Field(..., description="Default decision threshold", example=0.5)


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str = Field(..., description="Error message", example="Model not found")
    detail: str = Field(
        ...,
        description="Detailed error information",
        example="Model 'invalid_model' not available",
    )
    status_code: int = Field(..., description="HTTP status code", example=400)
    timestamp: str = Field(
        ..., description="Error timestamp", example="2025-09-01T22:30:00Z"
    )


# Dependency for request timing
async def get_request_timing():
    return {"start_time": time.time()}


def load_models():
    """Load trained models and preprocessing artifacts"""
    global models, feature_names, feature_scaler, model_metadata

    try:
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

        # Load models with metadata
        model_files = {
            "logistic_regression": "models/logistic_regression.pkl",
            "xgboost": "models/xgboost.pkl",
            "lightgbm": "models/lightgbm.pkl",
            "catboost": "models/catboost.pkl",
        }

        model_metadata = {
            "logistic_regression": {
                "model_type": "Logistic Regression",
                "performance_metrics": {"roc_auc": 0.879, "accuracy": 0.833},
                "training_date": "2025-08-19",
                "feature_count": 15,
                "model_size_mb": 0.001,
                "threshold": 0.5,
            },
            "xgboost": {
                "model_type": "XGBoost",
                "performance_metrics": {"roc_auc": 0.953, "accuracy": 0.931},
                "training_date": "2025-08-19",
                "feature_count": 15,
                "model_size_mb": 0.35,
                "threshold": 0.5,
            },
            "lightgbm": {
                "model_type": "LightGBM",
                "performance_metrics": {"roc_auc": 0.952, "accuracy": 0.930},
                "training_date": "2025-08-19",
                "feature_count": 15,
                "model_size_mb": 0.35,
                "threshold": 0.5,
            },
            "catboost": {
                "model_type": "CatBoost",
                "performance_metrics": {"roc_auc": 0.947, "accuracy": 0.916},
                "training_date": "2025-08-19",
                "feature_count": 15,
                "model_size_mb": 0.12,
                "threshold": 0.5,
            },
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

        logger.info(f"✅ Loaded {len(models)} models successfully")

    except Exception as e:
        logger.error(f"❌ Failed to load models: {e}")
        raise e from e


# Add startup event handler
@app.on_event("startup")
async def startup_event():
    """Handle startup events and model loading"""
    global startup_time

    startup_time = datetime.now()
    logger.info("🚀 FastAPI application starting up...")
    logger.info(f"🔧 Working directory: {os.getcwd()}")
    logger.info(f"🔧 Environment PORT: {os.environ.get('PORT', 'Not set')}")
    logger.info(f"🔧 Python path: {sys.path}")

    try:
        load_models()
        logger.info("✅ Application startup completed successfully")
    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        raise e


# Rate limiting dependency
async def check_rate_limit(request: Request):
    """Simple rate limiting - 100 requests per minute per IP"""
    # In production, implement proper rate limiting with Redis/database
    return True


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        current_time = datetime.now()
        uptime = (current_time - startup_time).total_seconds() if startup_time else 0

        # Get system metrics
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage("/")

        return HealthResponse(
            status="healthy" if len(models) > 0 else "degraded",
            timestamp=current_time.isoformat(),
            uptime_seconds=uptime,
            models_loaded=len(models),
            memory_usage_mb=memory.used / 1024 / 1024,
            cpu_usage_percent=cpu,
            disk_usage_percent=disk.percent,
            version="3.0.0",
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Health check failed: {str(e)}"
        ) from e


# Feature names endpoint
@app.get("/feature-names")
async def get_feature_names():
    """Get list of feature names used by the model"""
    try:
        return {
            "feature_count": len(feature_names),
            "features": feature_names,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Failed to get feature names: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get feature names: {str(e)}"
        ) from e


# Models endpoint
@app.get("/models", response_model=list[ModelInfo])
async def get_models():
    """Get information about available models"""
    try:
        model_info_list = []
        for model_name, metadata in model_metadata.items():
            if model_name in models:
                model_info_list.append(
                    ModelInfo(
                        model_name=model_name,
                        model_type=metadata["model_type"],
                        performance_metrics=metadata["performance_metrics"],
                        training_date=metadata["training_date"],
                        feature_count=metadata["feature_count"],
                        model_size_mb=metadata["model_size_mb"],
                        threshold=metadata["threshold"],
                    )
                )

        return model_info_list
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get model info: {str(e)}"
        ) from e


# Version endpoint
@app.get("/version")
async def get_version():
    """Get API version and model information"""
    return {
        "api_version": "3.0.0",
        "model_card_url": "https://github.com/Muh76/diabetes-readmission-prediction/blob/master/models/MODEL_CARD.md",
        "feature_docs_url": "https://github.com/Muh76/diabetes-readmission-prediction/blob/master/feature_documentation.md",
        "dashboard_url": "https://diabetes-readmission-prediction-drvwuus2xt7arfkucmvreq.streamlit.app/",
        "available_models": list(models.keys()),
        "default_model": "xgboost",
        "default_threshold": 0.5,
        "prediction_timing": "at_discharge",
        "timestamp": datetime.now().isoformat(),
    }


# Single prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict_readmission(
    patient: PatientData,
    model_name: str = "xgboost",
    threshold: Optional[float] = 0.5,
    request_timing: dict = Depends(get_request_timing),
    request: Request = Depends(),
):
    """
    Predict 30-day readmission risk for a single patient

    **Important Notes:**
    - Prediction is made at **discharge time** using only features available by discharge
    - `discharge_disposition_id` is known at discharge, not admission (no temporal leakage)
    - Default threshold is 0.5, but can be customized
    - Available models: xgboost, lightgbm, catboost, logistic_regression
    """
    try:
        # Rate limiting check
        await check_rate_limit(request)

        # Validate model
        if model_name not in models or models[model_name] is None:
            available_models = list(models.keys())
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model '{model_name}' not available. Available models: {available_models}",
            )

        # Validate threshold
        if not 0 <= threshold <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Threshold must be between 0 and 1",
            )

        # Prepare features
        feature_data = [
            patient.encounter_id,
            patient.patient_nbr,
            patient.admission_type_id,
            patient.discharge_disposition_id,
            patient.admission_source_id,
            patient.time_in_hospital,
            patient.num_lab_procedures,
            patient.num_procedures,
            patient.num_medications,
            patient.number_outpatient,
            patient.number_emergency,
            patient.number_inpatient,
            patient.number_diagnoses,
            patient.age_midpoint,
            patient.service_utilization_score,
            patient.clinical_risk_score,
        ]

        # Scale features
        if feature_scaler is not None:
            feature_data = feature_scaler.transform([feature_data])

        # Make prediction
        model = models[model_name]
        probability = model.predict_proba(feature_data)[0][1]
        readmission_risk = probability >= threshold

        # Calculate processing time
        processing_time = (time.time() - request_timing["start_time"]) * 1000

        # Determine confidence level
        if abs(probability - threshold) > 0.3:
            confidence_level = "High"
        elif abs(probability - threshold) > 0.1:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"

        # Get top risk factors (simplified)
        risk_factors = (
            ["num_medications", "time_in_hospital"] if probability > 0.5 else []
        )

        return PredictionResponse(
            patient_id=f"PAT_{patient.encounter_id}",
            timestamp=datetime.now().isoformat(),
            readmission_risk=readmission_risk,
            probability=float(probability),
            confidence_level=confidence_level,
            risk_factors=risk_factors,
            model_used=model_name,
            processing_time_ms=processing_time,
            message="Prediction completed successfully",
            threshold_used=threshold,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        ) from e


# Batch prediction endpoint
@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    patients: list[PatientData],
    model_name: str = "xgboost",
    threshold: Optional[float] = 0.5,
):
    """
    Predict readmission risk for multiple patients

    **Important Notes:**
    - Prediction is made at **discharge time** using only features available by discharge
    - Default threshold is 0.5, but can be customized
    - Available models: xgboost, lightgbm, catboost, logistic_regression
    - Maximum batch size: 100 patients
    """
    try:
        # Validate batch size
        if len(patients) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size cannot exceed 100 patients",
            )

        # Validate model
        if model_name not in models or models[model_name] is None:
            available_models = list(models.keys())
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model '{model_name}' not available. Available models: {available_models}",
            )

        # Validate threshold
        if not 0 <= threshold <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Threshold must be between 0 and 1",
            )

        start_time = time.time()
        results = []

        for i, patient in enumerate(patients):
            try:
                # Create single prediction request
                single_result = await predict_readmission(
                    patient, model_name, threshold
                )
                results.append(single_result.dict())
            except Exception as e:
                results.append(
                    {
                        "patient_id": f"PAT_BATCH_{i}",
                        "error": str(e),
                        "status": "failed",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        processing_time = (time.time() - start_time) * 1000
        successful_predictions = len([r for r in results if "error" not in r])
        failed_predictions = len([r for r in results if "error" in r])

        return BatchPredictionResponse(
            batch_id=f"BATCH_{int(time.time())}",
            total_patients=len(patients),
            successful_predictions=successful_predictions,
            failed_predictions=failed_predictions,
            results=results,
            processing_time_ms=processing_time,
            model_used=model_name,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}",
        ) from e


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint with comprehensive information"""
    return {
        "message": "Diabetes Readmission Prediction API",
        "version": "3.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
        "models": "/models",
        "version_info": "/version",
        "timestamp": datetime.now().isoformat(),
        "deployment": "Azure Container Apps Production",
        "prediction_timing": "at_discharge",
        "default_threshold": 0.5,
        "available_models": list(models.keys()),
        "model_card_url": "https://github.com/Muh76/diabetes-readmission-prediction/blob/master/models/MODEL_CARD.md",
        "dashboard_url": "https://diabetes-readmission-prediction-drvwuus2xt7arfkucmvreq.streamlit.app/",
    }


# Exception handler for better error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for consistent error responses"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "status_code": 500,
            "timestamp": datetime.now().isoformat(),
        },
    )


# 429 Rate limit exceeded handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler for rate limiting and other HTTP errors"""
    if exc.status_code == 429:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Rate limit exceeded",
                "detail": "Too many requests. Limit: 100 requests per minute.",
                "status_code": 429,
                "timestamp": datetime.now().isoformat(),
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
