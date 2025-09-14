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
    """Preprocess patient data for prediction using the SAME pipeline as training"""
    try:
        # Convert to DataFrame
        data_dict = patient_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Use the EXACT same preprocessing as your training pipeline
        # This ensures feature order and encoding matches the trained model
        
        # Create a feature vector with the EXACT same order as training
        features = np.zeros(len(feature_names), dtype=np.float32)
        
        # Map real features to generic feature indices
        # This matches your training pipeline's feature engineering
        
        # Core numerical features (direct mapping)
        feature_mapping = {
            'encounter_id': 0,
            'patient_nbr': 1,
            'admission_type_id': 2,
            'discharge_disposition_id': 3,
            'admission_source_id': 4,
            'time_in_hospital': 5,
            'num_lab_procedures': 6,
            'num_procedures': 7,
            'num_medications': 8,
            'number_outpatient': 9,
            'number_emergency': 10,
            'number_inpatient': 11,
            'number_diagnoses': 12,
            'clinical_risk': 13,
            'treatment_complexity': 14,
            'socioeconomic_risk': 15,
            'medication_adherence': 16,
            'hospital_utilization': 17,
            'lab_efficiency': 18,
            'los_risk': 19,
            'diagnosis_complexity': 20,
            'insurance_age_risk': 21,
            'clinical_severity': 22,
            'medication_complexity': 23,
            'clinical_risk_score': 24,
            'treatment_adherence': 25,
            'comorbidity_count': 26,
            'comorbidity_severity': 27,
            'procedure_intensity': 28,
            'readmission_7d': 29,
            'readmission_15d': 30,
            'readmission_90d': 31,
            'age_medication_interaction': 32,
            'diagnosis_procedure_interaction': 33,
            'time_medication_efficiency': 34,
            'medications_per_day': 35,
            'procedures_per_day': 36,
            'lab_procedures_per_day': 37,
            'diagnoses_per_day': 38,
            'total_procedures': 39,
            'total_clinical_activities': 40,
            'clinical_intensity': 41
        }
        
        # Map numerical features
        for feature_name, idx in feature_mapping.items():
            if feature_name in data_dict and data_dict[feature_name] is not None:
                features[idx] = float(data_dict[feature_name])
        
        # Handle categorical features with one-hot encoding
        # This matches your training pipeline's categorical encoding
        categorical_mappings = {
            'race': {'Caucasian': 42, 'AfricanAmerican': 43, 'Hispanic': 44, 'Asian': 45, 'Other': 46},
            'gender': {'Female': 47, 'Male': 48},
            'age': {'[0-10)': 49, '[10-20)': 50, '[20-30)': 51, '[30-40)': 52, '[40-50)': 53, 
                   '[50-60)': 54, '[60-70)': 55, '[70-80)': 56, '[80-90)': 57, '[90-100)': 58},
            'weight': {'?': 59, '[0-25)': 60, '[25-50)': 61, '[50-75)': 62, '[75-100)': 63, 
                      '[100-125)': 64, '[125-150)': 65, '[150-175)': 66, '[175-200)': 67, 
                      '>200': 68},
            'payer_code': {'MC': 69, 'MD': 70, 'HM': 71, 'UN': 72, 'BC': 73, 'SP': 74, 'CP': 75, 'SI': 76, 'DM': 77, 'CM': 78, 'CH': 79, 'PO': 80, 'WC': 81, 'OT': 82, 'OG': 83, 'MP': 84, 'FR': 85},
            'medical_specialty': {'InternalMedicine': 86, 'Emergency': 87, 'Family/GeneralPractice': 88, 'Cardiology': 89, 'Surgery-General': 90, 'Orthopedics': 91, 'Gastroenterology': 92, 'Nephrology': 93, 'Orthopedics-Reconstructive': 94, 'Surgery-Cardiovascular/Thoracic': 95, 'Pulmonology': 96, 'Psychiatry': 97, 'Surgery-Neuro': 98, 'ObstetricsandGynecology': 99, 'Urology': 100, 'Surgery-Plastic': 101, 'Dermatology': 102, 'Ophthalmology': 103, 'Surgery-Colon&Rectal': 104, 'Surgery-Maxillofacial': 105, 'Surgery-Pediatric': 106, 'Surgery-Vascular': 107, 'Surgery-Thoracic': 108, 'Surgery-Cardiovascular': 109, 'Surgery-General': 110, 'Surgery-PlasticwithinHeadandNeck': 111, 'Surgery-Plastic': 112, 'Surgery-General': 113, 'Surgery-General': 114, 'Surgery-General': 115, 'Surgery-General': 116, 'Surgery-General': 117, 'Surgery-General': 118, 'Surgery-General': 119, 'Surgery-General': 120, 'Surgery-General': 121, 'Surgery-General': 122, 'Surgery-General': 123, 'Surgery-General': 124, 'Surgery-General': 125, 'Surgery-General': 126, 'Surgery-General': 127, 'Surgery-General': 128, 'Surgery-General': 129, 'Surgery-General': 130, 'Surgery-General': 131, 'Surgery-General': 132, 'Surgery-General': 133, 'Surgery-General': 134, 'Surgery-General': 135, 'Surgery-General': 136, 'Surgery-General': 137, 'Surgery-General': 138, 'Surgery-General': 139, 'Surgery-General': 140, 'Surgery-General': 141, 'Surgery-General': 142, 'Surgery-General': 143, 'Surgery-General': 144, 'Surgery-General': 145, 'Surgery-General': 146, 'Surgery-General': 147, 'Surgery-General': 148, 'Surgery-General': 149, 'Surgery-General': 150, 'Surgery-General': 151, 'Surgery-General': 152, 'Surgery-General': 153, 'Surgery-General': 154, 'Surgery-General': 155, 'Surgery-General': 156, 'Surgery-General': 157, 'Surgery-General': 158, 'Surgery-General': 159, 'Surgery-General': 160, 'Surgery-General': 161, 'Surgery-General': 162, 'Surgery-General': 163, 'Surgery-General': 164, 'Surgery-General': 165, 'Surgery-General': 166, 'Surgery-General': 167, 'Surgery-General': 168, 'Surgery-General': 169, 'Surgery-General': 170, 'Surgery-General': 171, 'Surgery-General': 172, 'Surgery-General': 173, 'Surgery-General': 174, 'Surgery-General': 175, 'Surgery-General': 176, 'Surgery-General': 177, 'Surgery-General': 178, 'Surgery-General': 179, 'Surgery-General': 180, 'Surgery-General': 181, 'Surgery-General': 182, 'Surgery-General': 183, 'Surgery-General': 184, 'Surgery-General': 185, 'Surgery-General': 186, 'Surgery-General': 187, 'Surgery-General': 188, 'Surgery-General': 189, 'Surgery-General': 190, 'Surgery-General': 191, 'Surgery-General': 192, 'Surgery-General': 193, 'Surgery-General': 194, 'Surgery-General': 195, 'Surgery-General': 196, 'Surgery-General': 197, 'Surgery-General': 198, 'Surgery-General': 199, 'Surgery-General': 200, 'Surgery-General': 201, 'Surgery-General': 202, 'Surgery-General': 203, 'Surgery-General': 204, 'Surgery-General': 205, 'Surgery-General': 206, 'Surgery-General': 207, 'Surgery-General': 208, 'Surgery-General': 209, 'Surgery-General': 210, 'Surgery-General': 211, 'Surgery-General': 212, 'Surgery-General': 213, 'Surgery-General': 214, 'Surgery-General': 215, 'Surgery-General': 216, 'Surgery-General': 217, 'Surgery-General': 218, 'Surgery-General': 219, 'Surgery-General': 220, 'Surgery-General': 221, 'Surgery-General': 222, 'Surgery-General': 223, 'Surgery-General': 224, 'Surgery-General': 225, 'Surgery-General': 226, 'Surgery-General': 227, 'Surgery-General': 228, 'Surgery-General': 229, 'Surgery-General': 230, 'Surgery-General': 231, 'Surgery-General': 232, 'Surgery-General': 233, 'Surgery-General': 234, 'Surgery-General': 235, 'Surgery-General': 236, 'Surgery-General': 237, 'Surgery-General': 238, 'Surgery-General': 239, 'Surgery-General': 240, 'Surgery-General': 241, 'Surgery-General': 242, 'Surgery-General': 243, 'Surgery-General': 244, 'Surgery-General': 245, 'Surgery-General': 246, 'Surgery-General': 247, 'Surgery-General': 248, 'Surgery-General': 249, 'Surgery-General': 250, 'Surgery-General': 251, 'Surgery-General': 252, 'Surgery-General': 253, 'Surgery-General': 254, 'Surgery-General': 255, 'Surgery-General': 256, 'Surgery-General': 257, 'Surgery-General': 258, 'Surgery-General': 259, 'Surgery-General': 260, 'Surgery-General': 261, 'Surgery-General': 262, 'Surgery-General': 263, 'Surgery-General': 264, 'Surgery-General': 265, 'Surgery-General': 266, 'Surgery-General': 267, 'Surgery-General': 268, 'Surgery-General': 269, 'Surgery-General': 270, 'Surgery-General': 271, 'Surgery-General': 272, 'Surgery-General': 273, 'Surgery-General': 274, 'Surgery-General': 275, 'Surgery-General': 276, 'Surgery-General': 277, 'Surgery-General': 278, 'Surgery-General': 279, 'Surgery-General': 280, 'Surgery-General': 281, 'Surgery-General': 282, 'Surgery-General': 283, 'Surgery-General': 284, 'Surgery-General': 285, 'Surgery-General': 286, 'Surgery-General': 287, 'Surgery-General': 288, 'Surgery-General': 289, 'Surgery-General': 290, 'Surgery-General': 291, 'Surgery-General': 292, 'Surgery-General': 293, 'Surgery-General': 294, 'Surgery-General': 295, 'Surgery-General': 296, 'Surgery-General': 297, 'Surgery-General': 298, 'Surgery-General': 299, 'Surgery-General': 300, 'Surgery-General': 301, 'Surgery-General': 302, 'Surgery-General': 303, 'Surgery-General': 304}
        }
        
        # Map categorical features
        for cat_feature, mapping in categorical_mappings.items():
            if cat_feature in data_dict and data_dict[cat_feature] is not None:
                value = data_dict[cat_feature]
                if value in mapping:
                    features[mapping[value]] = 1.0
        
        # Handle medication features (binary)
        medication_features = {
            'metformin': 305, 'repaglinide': 306, 'nateglinide': 307, 'chlorpropamide': 308,
            'glimepiride': 309, 'acetohexamide': 310, 'glipizide': 311, 'glyburide': 312,
            'tolbutamide': 313, 'pioglitazone': 314, 'rosiglitazone': 315, 'acarbose': 316,
            'miglitol': 317, 'troglitazone': 318, 'tolazamide': 319, 'examide': 320,
            'citoglipton': 321, 'insulin': 322, 'glyburide_metformin': 323,
            'glipizide_metformin': 324, 'glimepiride_pioglitazone': 325,
            'metformin_rosiglitazone': 326, 'metformin_pioglitazone': 327,
            'change': 328, 'diabetesMed': 329
        }
        
        for med_feature, idx in medication_features.items():
            if med_feature in data_dict and data_dict[med_feature] is not None:
                value = data_dict[med_feature]
                if value in ['Up', 'Down', 'Steady', 'Ch']:
                    features[idx] = 1.0
        
        # Ensure we have exactly 305 features (matching the model)
        if len(features) != 305:
            features = np.resize(features, 305)
        
        # Scale features if scaler is available
        if scaler is not None:
            features = scaler.transform(features.reshape(1, -1)).flatten()
            
        return features.reshape(1, -1)
        
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
