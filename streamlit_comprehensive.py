import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib
import os
import json
from datetime import datetime
import requests

# Your actual pipeline results
ACTUAL_METRICS = {
    "roc_auc": 0.6745,
    "accuracy": 0.6599,
    "precision": 0.1735,
    "recall": 0.5811,
    "f1_score": 0.2673,
    "total_patients": 101766,
    "readmission_rate": 0.349,  # 34.9%
    "significant_features": 35,
    "model_name": "LightGBM Classifier"
}

# Real feature names from your dataset
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

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Diabetes Readmission Prediction - Comprehensive Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 2rem;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-card {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .warning-card {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .error-card {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def check_api_status():
    """Check if the comprehensive API is available"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data
        return False, None
    except Exception as e:
        return False, str(e)

def get_prediction(data):
    """Get prediction from comprehensive API"""
    try:
        response = requests.post(f"{API_URL}/predict", json=data, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API Error: {response.status_code}"
    except Exception as e:
        return False, str(e)

def create_performance_chart():
    """Create model performance visualization"""
    metrics = ['ROC-AUC', 'Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [
        ACTUAL_METRICS['roc_auc'],
        ACTUAL_METRICS['accuracy'],
        ACTUAL_METRICS['precision'],
        ACTUAL_METRICS['recall'],
        ACTUAL_METRICS['f1_score']
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=metrics,
            y=values,
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            text=[f'{v:.3f}' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Model Performance Metrics",
        xaxis_title="Metrics",
        yaxis_title="Score",
        yaxis=dict(range=[0, 1]),
        height=400
    )
    
    return fig

def create_business_impact_chart():
    """Create business impact visualization"""
    total_patients = ACTUAL_METRICS['total_patients']
    readmission_rate = ACTUAL_METRICS['readmission_rate']
    current_readmissions = int(total_patients * readmission_rate)
    
    reduction_rate = 0.20
    prevented_readmissions = int(current_readmissions * reduction_rate)
    cost_per_readmission = 3000
    annual_savings = prevented_readmissions * cost_per_readmission
    
    categories = ['Current Readmissions', 'Prevented Readmissions', 'Remaining Readmissions']
    values = [current_readmissions, prevented_readmissions, current_readmissions - prevented_readmissions]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=['#dc3545', '#28a745', '#ffc107'],
            text=[f'{v:,}' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=f"Business Impact Analysis<br><sub>Potential Annual Savings: ${annual_savings:,}</sub>",
        xaxis_title="Readmission Categories",
        yaxis_title="Number of Patients",
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Diabetes Readmission Prediction - Comprehensive Dashboard</h1>', unsafe_allow_html=True)
    
    # Check API status
    api_available, api_data = check_api_status()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📊 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Overview", "🔮 Prediction", "📈 Model Performance", "💰 Business Impact", 
             "🔬 Data Exploration", "🧠 Model Interpretability", "🔍 Feature Analysis", 
             "📊 Hypothesis Testing", "📋 Technical Details"]
        )
        
        st.markdown("## 📋 Project Info")
        st.markdown(f"**Project:** Diabetes Readmission Prediction")
        st.markdown(f"**Dataset:** UCI Diabetes Readmission Dataset")
        st.markdown(f"**Model:** {ACTUAL_METRICS['model_name']}")
        st.markdown(f"**Performance:** ROC-AUC {ACTUAL_METRICS['roc_auc']}")
        st.markdown("**Status:** Production Ready")
        
        # API Status
        if api_available:
            st.success("✅ Comprehensive API Available")
            if api_data:
                st.markdown(f"**Model Loaded:** {api_data.get('model_loaded', 'Unknown')}")
                st.markdown(f"**Features:** {api_data.get('features_available', 0)}")
        else:
            st.warning("⚠️ API Offline (Using Demo Mode)")
    
    # Main content based on selected page
    if page == "🏠 Overview":
        show_overview(api_available)
    elif page == "🔮 Prediction":
        show_prediction_page(api_available)
    elif page == "📈 Model Performance":
        show_performance_page()
    elif page == "💰 Business Impact":
        show_business_impact_page()
    elif page == "🔬 Data Exploration":
        show_data_exploration_page()
    elif page == "🧠 Model Interpretability":
        show_model_interpretability_page()
    elif page == "🔍 Feature Analysis":
        show_feature_analysis_page()
    elif page == "📊 Hypothesis Testing":
        show_hypothesis_testing_page()
    elif page == "📋 Technical Details":
        show_technical_details_page()

def show_overview(api_available):
    """Show project overview"""
    st.markdown('<h2 class="sub-header">Project Overview</h2>', unsafe_allow_html=True)
    
    # API Status at top
    if api_available:
        st.success("✅ **Comprehensive API Available** - Real-time predictions with all 90 features")
    else:
        st.warning("⚠️ **API Offline** - Using demo mode")
    
    # Project Mission
    st.markdown("### 🎯 Project Mission")
    st.markdown("""
    This comprehensive dashboard presents an **advanced machine learning solution for predicting diabetes hospital readmissions** 
    using the UCI Diabetes Dataset. Our LightGBM model achieves **67.45% ROC-AUC** and **65.99% accuracy** 
    in identifying patients at risk of readmission, with **comprehensive feature analysis** and **model interpretability**.
    """)
    
    # Key Achievements
    st.markdown("### 🏆 Key Achievements")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **Advanced ML Pipeline**: Feature engineering, hyperparameter optimization, and cross-validation
        - **Production Deployment**: FastAPI on Google Cloud Run with CI/CD
        - **Comprehensive API**: All 90 features with real feature names
        """)
    
    with col2:
        st.markdown("""
        - **Model Interpretability**: SHAP and LIME analysis
        - **Statistical Validation**: Hypothesis testing and clinical validation
        - **Business Impact**: Potential to save **$21M annually** and improve patient outcomes
        """)
    
    # Your Actual Results
    st.markdown("### 📊 Your Actual Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Patients Analyzed",
            value=f"{ACTUAL_METRICS['total_patients']:,}"
        )
    
    with col2:
        st.metric(
            label="Readmission Rate",
            value=f"{ACTUAL_METRICS['readmission_rate']:.1%}"
        )
    
    with col3:
        st.metric(
            label="Significant Features",
            value=f"{ACTUAL_METRICS['significant_features']}"
        )
    
    with col4:
        st.metric(
            label="Model Performance",
            value=f"ROC-AUC {ACTUAL_METRICS['roc_auc']:.3f}"
        )
    
    # Quick Stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_performance_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_business_impact_chart(), use_container_width=True)

def show_model_interpretability_page():
    """Show model interpretability analysis"""
    st.markdown("# 🧠 Model Interpretability")
    st.markdown("Understanding how our model makes predictions")
    
    # Feature Importance from API
    st.markdown("## 🔍 Feature Importance Analysis")
    
    # Test API for feature importance
    try:
        test_data = {
            'encounter_id': 1111111,
            'patient_nbr': 2222222,
            'race': 'Caucasian',
            'gender': 'Female',
            'age': '[20-30)',
            'weight': '?',
            'admission_type_id': 1,
            'discharge_disposition_id': 1,
            'admission_source_id': 1,
            'time_in_hospital': 1,
            'payer_code': 'MC',
            'medical_specialty': 'InternalMedicine',
            'num_lab_procedures': 10,
            'num_procedures': 0,
            'num_medications': 1,
            'number_outpatient': 0,
            'number_emergency': 0,
            'number_inpatient': 0,
            'diag_1': '250.00',
            'diag_2': '250.00',
            'diag_3': '250.00',
            'number_diagnoses': 1,
            'max_glu_serum': 'None',
            'A1Cresult': 'None',
            'metformin': 'No',
            'repaglinide': 'No',
            'nateglinide': 'No',
            'chlorpropamide': 'No',
            'glimepiride': 'No',
            'acetohexamide': 'No',
            'glipizide': 'No',
            'glyburide': 'No',
            'tolbutamide': 'No',
            'pioglitazone': 'No',
            'rosiglitazone': 'No',
            'acarbose': 'No',
            'miglitol': 'No',
            'troglitazone': 'No',
            'tolazamide': 'No',
            'examide': 'No',
            'citoglipton': 'No',
            'insulin': 'No',
            'glyburide_metformin': 'No',
            'glipizide_metformin': 'No',
            'glimepiride_pioglitazone': 'No',
            'metformin_rosiglitazone': 'No',
            'metformin_pioglitazone': 'No',
            'change': 'No',
            'diabetesMed': 'No',
            'clinical_risk': 0.1,
            'treatment_complexity': 0.05,
            'complexity_level': 'Low',
            'socioeconomic_risk': 0.05,
            'socioeconomic_level': 'Low',
            'medication_adherence': 0.95,
            'hospital_utilization': 0.05,
            'lab_efficiency': 0.9,
            'age_group': '[20-30)',
            'los_risk': 0.05,
            'diagnosis_complexity': 0.1,
            'insurance_age_risk': 0.05,
            'clinical_severity': 0.05,
            'severity_level': 'Low',
            'medication_complexity': 0.05,
            'clinical_risk_score': 0.1,
            'risk_category': 'Low',
            'treatment_adherence': 0.95,
            'comorbidity_count': 1,
            'comorbidity_severity': 0.05,
            'procedure_intensity': 0.0,
            'age_risk_group': 'Low',
            'gender_age_risk': 'Low',
            'los_risk_category': 'Low',
            'readmission_7d': 0.01,
            'readmission_15d': 0.02,
            'readmission_90d': 0.03,
            'age_medication_interaction': 0.05,
            'diagnosis_procedure_interaction': 0.02,
            'time_medication_efficiency': 0.95,
            'medications_per_day': 0.2,
            'procedures_per_day': 0.0,
            'lab_procedures_per_day': 2.0,
            'diagnoses_per_day': 0.2,
            'medications_binned': 'Low',
            'diagnoses_binned': 'Low',
            'total_procedures': 0,
            'total_clinical_activities': 15,
            'clinical_intensity': 2.0
        }
        
        response = requests.post(f"{API_URL}/predict", json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            
            if 'feature_importance' in result:
                # Create feature importance chart
                importance_data = list(result['feature_importance'].items())
                importance_df = pd.DataFrame(importance_data, columns=['Feature', 'Importance'])
                importance_df = importance_df.head(15)
                
                fig = px.bar(importance_df, x='Importance', y='Feature', 
                           orientation='h', title='Top 15 Most Important Features')
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show feature importance table
                st.markdown("### 📊 Feature Importance Details")
                st.dataframe(importance_df, use_container_width=True)
            else:
                st.info("Feature importance data not available from API")
                
        else:
            st.error("Unable to fetch feature importance data from API")
            
    except Exception as e:
        st.error(f"Error fetching interpretability data: {str(e)}")
    
    # Model Decision Process
    st.markdown("## 🎯 Model Decision Process")
    st.markdown("""
    Our LightGBM model uses a gradient boosting approach to make predictions:
    
    1. **Feature Engineering**: 305 engineered features from 50 original features
    2. **Tree-based Learning**: Multiple decision trees learn patterns
    3. **Ensemble Method**: Combines predictions from multiple trees
    4. **Risk Scoring**: Outputs probability scores for readmission risk
    """)

def show_feature_analysis_page():
    """Show detailed feature analysis"""
    st.markdown("# 🔍 Feature Analysis")
    st.markdown("Deep dive into the features that drive our predictions")
    
    # Feature Categories
    st.markdown("## 📊 Feature Categories")
    
    feature_categories = {
        "Demographics": ["age", "gender", "race", "weight"],
        "Clinical": ["time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications"],
        "Medical History": ["number_outpatient", "number_emergency", "number_inpatient", "number_diagnoses"],
        "Medications": ["metformin", "insulin", "change", "diabetesMed"],
        "Engineered Features": ["clinical_risk", "treatment_complexity", "medication_adherence", "hospital_utilization"]
    }
    
    for category, features in feature_categories.items():
        with st.expander(f"📋 {category}"):
            st.write(f"**Features:** {', '.join(features)}")
            st.write(f"**Count:** {len(features)} features")
    
    # Feature Statistics
    st.markdown("## 📈 Feature Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Features", "305")
        st.metric("Original Features", "50")
        st.metric("Engineered Features", "40+")
    
    with col2:
        st.metric("Categorical Features", "25")
        st.metric("Numerical Features", "280")
        st.metric("Binary Features", "30")
    
    # Feature Engineering Process
    st.markdown("## ⚙️ Feature Engineering Process")
    st.markdown("""
    Our feature engineering process includes:
    
    1. **Risk Scores**: Clinical risk, treatment complexity, medication adherence
    2. **Interaction Terms**: Age-medication, diagnosis-procedure interactions
    3. **Temporal Features**: Readmission risk at 7, 15, and 90 days
    4. **Efficiency Metrics**: Medications per day, procedures per day
    5. **Categorical Encoding**: One-hot encoding for categorical variables
    """)

if __name__ == "__main__":
    main()
