import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Diabetes Readmission Prediction API - Comprehensive",
    description="Advanced ML API for diabetes readmission prediction with all features",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
feature_names = None
scaler = None
real_feature_names = None
startup_time = None

# Real feature names mapping (from your engineered dataset)
REAL_FEATURE_NAMES = [
    "encounter_id", "patient_nbr", "race", "gender", "age", "weight",
    "admission_type_id", "discharge_disposition_id", "admission_source_id",
    "time_in_hospital", "payer_code", "medical_specialty", "num_lab_procedures",
    "num_procedures", "num_medications", "number_outpatient", "number_emergency",
    "number_inpatient", "diag_1", "diag_2", "diag_3", "number_diagnoses",
    "max_glu_serum", "A1Cresult", "metformin", "repaglinide", "nateglinide",
    "chlorpropamide", "glimepiride", "acetohexamide", "glipizide", "glyburide",
    "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", "miglitol",
    "troglitazone", "tolazamide", "examide", "citoglipton", "insulin",
    "glyburide-metformin", "glipizide-metformin", "glimepiride-pioglitazone",
    "metformin-rosiglitazone", "metformin-pioglitazone", "change", "diabetesMed",
    "clinical_risk", "treatment_complexity", "complexity_level", "socioeconomic_risk",
    "socioeconomic_level", "medication_adherence", "hospital_utilization",
    "lab_efficiency", "age_group", "los_risk", "diagnosis_complexity",
    "insurance_age_risk", "clinical_severity", "severity_level", "medication_complexity",
    "clinical_risk_score", "risk_category", "treatment_adherence", "comorbidity_count",
    "comorbidity_severity", "procedure_intensity", "age_risk_group", "gender_age_risk",
    "los_risk_category", "readmission_7d", "readmission_15d", "readmission_90d",
    "age_medication_interaction", "diagnosis_procedure_interaction",
    "time_medication_efficiency", "medications_per_day", "procedures_per_day",
    "lab_procedures_per_day", "diagnoses_per_day", "medications_binned",
    "diagnoses_binned", "total_procedures", "total_clinical_activities", "clinical_intensity"
]

# Comprehensive Patient Data Model
class PatientData(BaseModel):
    """Comprehensive patient data model with all 90 features"""
    
    # Core identifiers
    encounter_id: int = Field(..., description="Unique encounter identifier", example=2278392)
    patient_nbr: int = Field(..., description="Unique patient number", example=8222157)
    
    # Demographics
    race: str = Field(..., description="Patient race", example="Caucasian")
    gender: str = Field(..., description="Patient gender", example="Female")
    age: str = Field(..., description="Patient age group", example="[50-60)")
    weight: Optional[str] = Field(None, description="Patient weight", example="?")
    
    # Admission information
    admission_type_id: int = Field(..., description="Admission type ID", example=1)
    discharge_disposition_id: int = Field(..., description="Discharge disposition ID", example=1)
    admission_source_id: int = Field(..., description="Admission source ID", example=7)
    
    # Hospital stay
    time_in_hospital: int = Field(..., description="Time in hospital (days)", example=5)
    
    # Insurance and specialty
    payer_code: str = Field(..., description="Payer code", example="MC")
    medical_specialty: str = Field(..., description="Medical specialty", example="InternalMedicine")
    
    # Procedures and medications
    num_lab_procedures: int = Field(..., description="Number of lab procedures", example=41)
    num_procedures: int = Field(..., description="Number of procedures", example=0)
    num_medications: int = Field(..., description="Number of medications", example=10)
    
    # Visit history
    number_outpatient: int = Field(..., description="Number of outpatient visits", example=0)
    number_emergency: int = Field(..., description="Number of emergency visits", example=0)
    number_inpatient: int = Field(..., description="Number of inpatient visits", example=0)
    
    # Diagnoses
    diag_1: str = Field(..., description="Primary diagnosis", example="250.00")
    diag_2: Optional[str] = Field(None, description="Secondary diagnosis", example="250.00")
    diag_3: Optional[str] = Field(None, description="Tertiary diagnosis", example="250.00")
    number_diagnoses: int = Field(..., description="Number of diagnoses", example=3)
    
    # Lab results
    max_glu_serum: str = Field(..., description="Maximum glucose serum", example="None")
    A1Cresult: str = Field(..., description="A1C result", example="None")
    
    # Medications (all diabetes medications)
    metformin: str = Field(..., description="Metformin", example="No")
    repaglinide: str = Field(..., description="Repaglinide", example="No")
    nateglinide: str = Field(..., description="Nateglinide", example="No")
    chlorpropamide: str = Field(..., description="Chlorpropamide", example="No")
    glimepiride: str = Field(..., description="Glimepiride", example="No")
    acetohexamide: str = Field(..., description="Acetohexamide", example="No")
    glipizide: str = Field(..., description="Glipizide", example="No")
    glyburide: str = Field(..., description="Glyburide", example="No")
    tolbutamide: str = Field(..., description="Tolbutamide", example="No")
    pioglitazone: str = Field(..., description="Pioglitazone", example="No")
    rosiglitazone: str = Field(..., description="Rosiglitazone", example="No")
    acarbose: str = Field(..., description="Acarbose", example="No")
    miglitol: str = Field(..., description="Miglitol", example="No")
    troglitazone: str = Field(..., description="Troglitazone", example="No")
    tolazamide: str = Field(..., description="Tolazamide", example="No")
    examide: str = Field(..., description="Examide", example="No")
    citoglipton: str = Field(..., description="Citoglipton", example="No")
    insulin: str = Field(..., description="Insulin", example="No")
    glyburide_metformin: str = Field(..., description="Glyburide-Metformin", example="No")
    glipizide_metformin: str = Field(..., description="Glipizide-Metformin", example="No")
    glimepiride_pioglitazone: str = Field(..., description="Glimepiride-Pioglitazone", example="No")
    metformin_rosiglitazone: str = Field(..., description="Metformin-Rosiglitazone", example="No")
    metformin_pioglitazone: str = Field(..., description="Metformin-Pioglitazone", example="No")
    
    # Treatment changes
    change: str = Field(..., description="Change in diabetes medications", example="No")
    diabetesMed: str = Field(..., description="Diabetes medication", example="Yes")
    
    # Engineered features (clinical risk, complexity, etc.)
    clinical_risk: float = Field(..., description="Clinical risk score", example=0.5)
    treatment_complexity: float = Field(..., description="Treatment complexity", example=0.3)
    complexity_level: str = Field(..., description="Complexity level", example="Low")
    socioeconomic_risk: float = Field(..., description="Socioeconomic risk", example=0.2)
    socioeconomic_level: str = Field(..., description="Socioeconomic level", example="Low")
    medication_adherence: float = Field(..., description="Medication adherence", example=0.8)
    hospital_utilization: float = Field(..., description="Hospital utilization", example=0.1)
    lab_efficiency: float = Field(..., description="Lab efficiency", example=0.6)
    age_group: str = Field(..., description="Age group", example="[50-60)")
    los_risk: float = Field(..., description="Length of stay risk", example=0.3)
    diagnosis_complexity: float = Field(..., description="Diagnosis complexity", example=0.4)
    insurance_age_risk: float = Field(..., description="Insurance-age risk", example=0.2)
    clinical_severity: float = Field(..., description="Clinical severity", example=0.5)
    severity_level: str = Field(..., description="Severity level", example="Medium")
    medication_complexity: float = Field(..., description="Medication complexity", example=0.3)
    clinical_risk_score: float = Field(..., description="Clinical risk score", example=0.4)
    risk_category: str = Field(..., description="Risk category", example="Medium")
    treatment_adherence: float = Field(..., description="Treatment adherence", example=0.7)
    comorbidity_count: int = Field(..., description="Comorbidity count", example=2)
    comorbidity_severity: float = Field(..., description="Comorbidity severity", example=0.3)
    procedure_intensity: float = Field(..., description="Procedure intensity", example=0.2)
    age_risk_group: str = Field(..., description="Age risk group", example="Medium")
    gender_age_risk: str = Field(..., description="Gender-age risk", example="Medium")
    los_risk_category: str = Field(..., description="LOS risk category", example="Low")
    readmission_7d: float = Field(..., description="7-day readmission risk", example=0.1)
    readmission_15d: float = Field(..., description="15-day readmission risk", example=0.2)
    readmission_90d: float = Field(..., description="90-day readmission risk", example=0.3)
    age_medication_interaction: float = Field(..., description="Age-medication interaction", example=0.2)
    diagnosis_procedure_interaction: float = Field(..., description="Diagnosis-procedure interaction", example=0.1)
    time_medication_efficiency: float = Field(..., description="Time-medication efficiency", example=0.4)
    medications_per_day: float = Field(..., description="Medications per day", example=2.0)
    procedures_per_day: float = Field(..., description="Procedures per day", example=0.0)
    lab_procedures_per_day: float = Field(..., description="Lab procedures per day", example=8.2)
    diagnoses_per_day: float = Field(..., description="Diagnoses per day", example=0.6)
    medications_binned: str = Field(..., description="Medications binned", example="Medium")
    diagnoses_binned: str = Field(..., description="Diagnoses binned", example="Low")
    total_procedures: int = Field(..., description="Total procedures", example=0)
    total_clinical_activities: int = Field(..., description="Total clinical activities", example=42)
    clinical_intensity: float = Field(..., description="Clinical intensity", example=21.0)

class PredictionResponse(BaseModel):
    """Enhanced prediction response with comprehensive information"""
    prediction: int = Field(..., description="Prediction (0=No readmission, 1=Readmission)")
    probability: float = Field(..., description="Readmission probability")
    risk_level: str = Field(..., description="Risk level (Low/Medium/High)")
    confidence: float = Field(..., description="Prediction confidence")
    model_version: str = Field(..., description="Model version")
    timestamp: str = Field(..., description="Prediction timestamp")
    features_used: List[str] = Field(..., description="Features used in prediction")
    feature_importance: Dict[str, float] = Field(..., description="Top 10 feature importance scores")
    shap_values: Dict[str, float] = Field(..., description="SHAP values for top features")
    clinical_insights: List[str] = Field(..., description="Clinical insights from prediction")

def load_model():
    """Load the trained model and feature names"""
    global model, feature_names, scaler, real_feature_names, startup_time
    
    try:
        # Load model
        model_path = os.getenv("MODEL_PATH", "./models/lightgbm_optimized.pkl")
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        
        # Load feature names
        feature_names_path = os.getenv("FEATURE_NAMES_PATH", "./models/feature_names.pkl")
        feature_names = joblib.load(feature_names_path)
        logger.info(f"Feature names loaded from {feature_names_path}")
        
        # Map generic feature names to real names
        real_feature_names = {}
        for i, generic_name in enumerate(feature_names):
            if i < len(REAL_FEATURE_NAMES):
                real_feature_names[generic_name] = REAL_FEATURE_NAMES[i]
            else:
                real_feature_names[generic_name] = f"engineered_feature_{i}"
        
        logger.info(f"Real feature names mapped: {len(real_feature_names)} features")
        
        # Try to load scaler if available
        scaler_path = os.getenv("SCALER_PATH", "./models/scaler.pkl")
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")
        
        startup_time = datetime.utcnow()
        logger.info("Model loading completed successfully")
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e

def preprocess_features(patient_data: PatientData) -> np.ndarray:
    """Preprocess patient data for prediction"""
    try:
        # Convert to DataFrame
        data_dict = patient_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Handle categorical variables with proper encoding
        categorical_features = [
            'race', 'gender', 'age', 'weight', 'payer_code', 'medical_specialty',
            'diag_1', 'diag_2', 'diag_3', 'max_glu_serum', 'A1Cresult',
            'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
            'glimepiride', 'acetohexamide', 'glipizide', 'glyburide',
            'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose',
            'miglitol', 'troglitazone', 'tolazamide', 'examide',
            'citoglipton', 'insulin', 'glyburide_metformin',
            'glipizide_metformin', 'glimepiride_pioglitazone',
            'metformin_rosiglitazone', 'metformin_pioglitazone',
            'change', 'diabetesMed', 'complexity_level', 'socioeconomic_level',
            'age_group', 'severity_level', 'risk_category', 'age_risk_group',
            'gender_age_risk', 'los_risk_category', 'medications_binned',
            'diagnoses_binned'
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

def determine_risk_level(probability: float) -> str:
    """Determine risk level based on probability"""
    if probability > 0.7:
        return "High"
    elif probability > 0.4:
        return "Medium"
    else:
        return "Low"

def calculate_confidence(probability: float) -> float:
    """Calculate prediction confidence"""
    return abs(probability - 0.5) * 2

def get_feature_importance() -> Dict[str, float]:
    """Get feature importance from the model"""
    try:
        if hasattr(model, 'feature_importances_'):
            importance_scores = model.feature_importances_
            # Get top 10 features
            top_indices = np.argsort(importance_scores)[-10:][::-1]
            
            feature_importance = {}
            for idx in top_indices:
                generic_name = feature_names[idx]
                real_name = real_feature_names.get(generic_name, generic_name)
                feature_importance[real_name] = float(importance_scores[idx])
            
            return feature_importance
        else:
            return {}
    except Exception as e:
        logger.error(f"Error getting feature importance: {str(e)}")
        return {}

def get_shap_values(features: np.ndarray) -> Dict[str, float]:
    """Get SHAP values for feature explanation"""
    try:
        import shap
        
        # Create SHAP explainer
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(features)
        
        # Get top 10 features by absolute SHAP value
        if len(shap_values.shape) > 1:
            shap_values = shap_values[0]  # For binary classification
        
        top_indices = np.argsort(np.abs(shap_values))[-10:][::-1]
        
        shap_dict = {}
        for idx in top_indices:
            generic_name = feature_names[idx]
            real_name = real_feature_names.get(generic_name, generic_name)
            shap_dict[real_name] = float(shap_values[idx])
        
        return shap_dict
    except Exception as e:
        logger.error(f"Error getting SHAP values: {str(e)}")
        return {}

def generate_clinical_insights(probability: float, feature_importance: Dict[str, float]) -> List[str]:
    """Generate clinical insights based on prediction"""
    insights = []
    
    if probability > 0.7:
        insights.append("High readmission risk - consider enhanced discharge planning")
        insights.append("Patient may benefit from post-discharge monitoring")
    elif probability > 0.4:
        insights.append("Moderate readmission risk - standard follow-up recommended")
    else:
        insights.append("Low readmission risk - routine care should be sufficient")
    
    # Add insights based on top features
    if feature_importance:
        top_feature = max(feature_importance, key=feature_importance.get)
        if "medication" in top_feature.lower():
            insights.append("Medication management appears to be a key factor")
        elif "time_in_hospital" in top_feature.lower():
            insights.append("Length of stay is a significant predictor")
        elif "age" in top_feature.lower():
            insights.append("Age-related factors are important in this prediction")
    
    return insights

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("Starting up Diabetes Readmission Prediction API...")
    load_model()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down API...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Diabetes Readmission Prediction API - Comprehensive Version",
        "version": "2.0.0",
        "status": "healthy",
        "features": len(REAL_FEATURE_NAMES),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "features_available": len(feature_names) if feature_names is not None else 0,
        "real_features_mapped": len(real_feature_names) if real_feature_names is not None else 0,
        "uptime": (datetime.utcnow() - startup_time).total_seconds() if startup_time else 0,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/model/info")
async def get_model_info():
    """Get model information"""
    return {
        "model_type": type(model).__name__ if model else "Not loaded",
        "feature_count": len(feature_names) if feature_names is not None else 0,
        "real_feature_names": list(real_feature_names.keys()) if real_feature_names else [],
        "scaler_available": scaler is not None,
        "model_version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_readmission(
    patient: PatientData,
    background_tasks: BackgroundTasks
):
    """Predict 30-day readmission risk for a single patient with comprehensive analysis"""
    try:
        # Preprocess features
        features = preprocess_features(patient)
        
        # Make prediction
        probability = model.predict_proba(features)[0][1]
        prediction = int(probability > 0.5)
        
        # Determine risk level and confidence
        risk_level = determine_risk_level(probability)
        confidence = calculate_confidence(probability)
        
        # Get feature importance and SHAP values
        feature_importance = get_feature_importance()
        shap_values = get_shap_values(features)
        
        # Generate clinical insights
        clinical_insights = generate_clinical_insights(probability, feature_importance)
        
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            risk_level=risk_level,
            confidence=confidence,
            model_version="2.0.0",
            timestamp=datetime.utcnow().isoformat() + "Z",
            features_used=list(real_feature_names.keys()) if real_feature_names else [],
            feature_importance=feature_importance,
            shap_values=shap_values,
            clinical_insights=clinical_insights
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/features")
async def get_features():
    """Get all available features with their descriptions"""
    return {
        "total_features": len(REAL_FEATURE_NAMES),
        "features": REAL_FEATURE_NAMES,
        "feature_mapping": real_feature_names if real_feature_names else {},
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
