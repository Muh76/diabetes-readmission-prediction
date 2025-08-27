# 🚀 API DOCUMENTATION - DIABETIC READMISSION PREDICTION SYSTEM

**API Version:** 1.0
**Base URL:** `https://diabetes-ml-api.azurecontainerapps.io` (Production URL)
**Status:** Production Deployed ✅
**Last Updated:** August 2025

---

## 📋 API OVERVIEW

The Diabetic Readmission Prediction API provides machine learning-powered risk assessment for diabetic patients. Built with FastAPI, it offers high-performance prediction endpoints with comprehensive monitoring and validation.

### **🔑 Key Features:**
- **Real-time Predictions** - Sub-second response times
- **Batch Processing** - Handle multiple patients efficiently
- **Model Management** - Multiple ML models with automatic selection
- **Health Monitoring** - Comprehensive system health checks
- **Audit Logging** - Full request/response tracking

---

## 🏗️ API ARCHITECTURE

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │    │   FastAPI       │    │   ML Models     │
│   (Streamlit)   │◄──►│   Backend       │◄──►│   (XGBoost,     │
│                 │    │   (Port 8000)   │    │    LightGBM,    │
└─────────────────┘    └─────────────────┘    │    CatBoost)    │
                                              └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Monitoring    │    │   Data          │    │   Feature       │
│   (Prometheus)  │    │   Validation    │    │   Engineering   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🔌 API ENDPOINTS

### **1. 🏠 ROOT ENDPOINT**

#### **GET /** - API Information
Returns basic API information and status.

**Request:**
```bash
curl -X GET "https://diabetes-ml-api.azurecontainerapps.io/"
```

**Response:**
```json
{
  "name": "Diabetic Readmission Prediction API",
  "version": "1.0.0",
  "status": "operational",
  "description": "ML-powered API for predicting diabetic patient readmission risk",
  "endpoints": {
    "health": "/health",
    "models": "/models",
    "predict": "/predict",
    "predict/batch": "/predict/batch"
  },
  "documentation": "/docs",
  "timestamp": "2025-08-19T18:42:56.143056"
}
```

---

### **2. 🏥 HEALTH CHECK ENDPOINT**

#### **GET /health** - Comprehensive Health Check
Returns detailed system health information including model status, resource usage, and performance metrics.

**Request:**
```bash
curl -X GET "https://diabetes-ml-api.azurecontainerapps.io/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-19T18:42:56.143056",
  "uptime_seconds": 12345.67,
  "models_loaded": 5,
  "memory_usage_mb": 8338.03,
  "cpu_usage_percent": 16.0,
  "disk_usage_percent": 4.49,
  "model_performance": {
    "last_accuracy_check": "2025-08-19T18:00:00",
    "current_accuracy": 0.9312,
    "prediction_count_today": 1247
  },
  "system_health": {
    "database": "healthy",
    "cache": "healthy",
    "external_services": "healthy"
  }
}
```

**Health Status Codes:**
- `healthy` - All systems operational
- `degraded` - Some systems experiencing issues
- `unhealthy` - Critical systems down

---

### **3. 🤖 MODEL INFORMATION ENDPOINT**

#### **GET /models** - Model Details
Returns information about all available ML models including performance metrics and status.

**Request:**
```bash
curl -X GET "https://diabetes-ml-api.azurecontainerapps.io/models"
```

**Response:**
```json
{
  "models": [
    {
      "name": "XGBoost (Optimized)",
      "version": "1.0.0",
      "status": "active",
      "performance": {
        "accuracy": 0.9312,
        "precision": 0.9952,
        "recall": 0.8666,
        "f1_score": 0.9265,
        "roc_auc": 0.9532
      },
      "last_updated": "2025-08-19T18:00:00",
      "training_data_size": 144655,
      "features_count": 150
    },
    {
      "name": "Random Forest (Optimized)",
      "version": "1.0.0",
      "status": "active",
      "performance": {
        "accuracy": 0.9244,
        "precision": 0.9837,
        "recall": 0.8631,
        "f1_score": 0.9195,
        "roc_auc": 0.9530
      },
      "last_updated": "2025-08-19T18:00:00",
      "training_data_size": 144655,
      "features_count": 150
    }
  ],
  "active_model": "XGBoost (Optimized)",
  "model_selection_criteria": "highest_accuracy"
}
```

---

### **4. 🔮 SINGLE PREDICTION ENDPOINT**

#### **POST /predict** - Single Patient Prediction
Predicts readmission risk for a single patient using the best-performing model.

**Request:**
```bash
curl -X POST "https://diabetes-ml-api.azurecontainerapps.io/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P001",
    "age": 65,
    "gender": "F",
    "race": "Caucasian",
    "admission_type": "Emergency",
    "discharge_disposition": "Home",
    "admission_source": "Physician Referral",
    "time_in_hospital": 4,
    "medical_specialty": "Cardiology",
    "num_lab_procedures": 25,
    "num_procedures": 2,
    "num_medications": 15,
    "number_outpatient": 3,
    "number_emergency": 1,
    "number_inpatient": 1,
    "diag_1": "250.00",
    "diag_2": "401.9",
    "diag_3": "272.4",
    "number_diagnoses": 8,
    "max_glu_serum": ">200",
    "A1Cresult": ">7",
    "metformin": "No",
    "repaglinide": "No",
    "nateglinide": "No",
    "chlorpropamide": "No",
    "glimepiride": "No",
    "acetohexamide": "No",
    "glipizide": "No",
    "glyburide": "No",
    "tolbutamide": "No",
    "pioglitazone": "No",
    "rosiglitazone": "No",
    "acarbose": "No",
    "miglitol": "No",
    "troglitazone": "No",
    "tolazamide": "No",
    "examide": "No",
    "citoglipton": "No",
    "insulin": "No",
    "glyburide-metformin": "No",
    "glipizide-metformin": "No",
    "glimepiride-pioglitazone": "No",
    "metformin-rosiglitazone": "No",
    "metformin-pioglitazone": "No",
    "change": "No",
    "diabetesMed": "Yes",
    "readmitted": null
  }'
```

**Response:**
```json
{
  "prediction_id": "pred_12345",
  "patient_id": "P001",
  "timestamp": "2025-08-19T18:42:56.143056",
  "model_used": "XGBoost (Optimized)",
  "prediction": {
    "readmission_risk": 0.78,
    "risk_category": "HIGH",
    "confidence_score": 0.89,
    "risk_factors": [
      "age_over_65",
      "multiple_diagnoses",
      "high_medication_count",
      "previous_readmissions"
    ]
  },
  "recommendations": [
    "Schedule follow-up within 7 days",
    "Review medication compliance",
    "Consider care coordination services",
    "Monitor blood glucose levels closely"
  ],
  "processing_time_ms": 45
}
```

**Risk Categories:**
- `LOW` (0.0 - 0.3): Minimal risk, standard care
- `MEDIUM` (0.3 - 0.6): Moderate risk, enhanced monitoring
- `HIGH` (0.6 - 0.8): High risk, intervention recommended
- `CRITICAL` (0.8 - 1.0): Critical risk, immediate action required

---

### **5. 📊 BATCH PREDICTION ENDPOINT**

#### **POST /predict/batch** - Multiple Patient Predictions
Processes multiple patients efficiently for bulk risk assessment.

**Request:**
```bash
curl -X POST "https://diabetes-ml-api.azurecontainerapps.io/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "patients": [
      {
        "patient_id": "P001",
        "age": 65,
        "gender": "F",
        "race": "Caucasian",
        "admission_type": "Emergency",
        "discharge_disposition": "Home",
        "admission_source": "Physician Referral",
        "time_in_hospital": 4,
        "medical_specialty": "Cardiology",
        "num_lab_procedures": 25,
        "num_procedures": 2,
        "num_medications": 15,
        "number_outpatient": 3,
        "number_emergency": 1,
        "number_inpatient": 1,
        "diag_1": "250.00",
        "diag_2": "401.9",
        "diag_3": "272.4",
        "number_diagnoses": 8,
        "max_glu_serum": ">200",
        "A1Cresult": ">7",
        "metformin": "No",
        "repaglinide": "No",
        "nateglinide": "No",
        "chlorpropamide": "No",
        "glimepiride": "No",
        "acetohexamide": "No",
        "glipizide": "No",
        "glyburide": "No",
        "tolbutamide": "No",
        "pioglitazone": "No",
        "rosiglitazone": "No",
        "acarbose": "No",
        "miglitol": "No",
        "troglitazone": "No",
        "tolazamide": "No",
        "examide": "No",
        "citoglipton": "No",
        "insulin": "No",
        "glyburide-metformin": "No",
        "glipizide-metformin": "No",
        "glimepiride-pioglitazone": "No",
        "metformin-rosiglitazone": "No",
        "metformin-pioglitazone": "No",
        "change": "No",
        "diabetesMed": "Yes",
        "readmitted": null
      },
      {
        "patient_id": "P002",
        "age": 45,
        "gender": "M",
        "race": "African American",
        "admission_type": "Elective",
        "discharge_disposition": "Home",
        "admission_source": "Physician Referral",
        "time_in_hospital": 2,
        "medical_specialty": "Endocrinology",
        "num_lab_procedures": 15,
        "num_procedures": 1,
        "num_medications": 8,
        "number_outpatient": 2,
        "number_emergency": 0,
        "number_inpatient": 0,
        "diag_1": "250.01",
        "diag_2": "272.4",
        "diag_3": null,
        "number_diagnoses": 4,
        "max_glu_serum": ">200",
        "A1Cresult": ">7",
        "metformin": "Yes",
        "repaglinide": "No",
        "nateglinide": "No",
        "chlorpropamide": "No",
        "glimepiride": "No",
        "acetohexamide": "No",
        "glipizide": "No",
        "glyburide": "No",
        "tolbutamide": "No",
        "pioglitazone": "No",
        "rosiglitazone": "No",
        "acarbose": "No",
        "miglitol": "No",
        "troglitazone": "No",
        "tolazamide": "No",
        "examide": "No",
        "citoglipton": "No",
        "insulin": "No",
        "glyburide-metformin": "No",
        "glipizide-metformin": "No",
        "glimepiride-pioglitazone": "No",
        "metformin-rosiglitazone": "No",
        "metformin-pioglitazone": "No",
        "change": "No",
        "diabetesMed": "Yes",
        "readmitted": null
      }
    ]
  }'
```

**Response:**
```json
{
  "batch_id": "batch_67890",
  "timestamp": "2025-08-19T18:42:56.143056",
  "total_patients": 2,
  "processing_time_ms": 89,
  "model_used": "XGBoost (Optimized)",
  "predictions": [
    {
      "patient_id": "P001",
      "readmission_risk": 0.78,
      "risk_category": "HIGH",
      "confidence_score": 0.89
    },
    {
      "patient_id": "P002",
      "readmission_risk": 0.23,
      "risk_category": "LOW",
      "confidence_score": 0.92
    }
  ],
  "summary": {
    "high_risk_count": 1,
    "medium_risk_count": 0,
    "low_risk_count": 1,
    "average_risk": 0.51
  }
}
```

---

## 📊 DATA SCHEMAS

### **Patient Data Schema**
```json
{
  "patient_id": "string (required)",
  "age": "integer (1-100)",
  "gender": "string (M/F)",
  "race": "string (Caucasian/African American/Hispanic/Asian/Other)",
  "admission_type": "string (Emergency/Urgent/Elective/Newborn)",
  "discharge_disposition": "string (Home/Transfer/Other)",
  "admission_source": "string (Physician Referral/Emergency Room/Transfer)",
  "time_in_hospital": "integer (1-14)",
  "medical_specialty": "string (Cardiology/Endocrinology/Internal Medicine/etc)",
  "num_lab_procedures": "integer (0-100)",
  "num_procedures": "integer (0-10)",
  "num_medications": "integer (0-50)",
  "number_outpatient": "integer (0-50)",
  "number_emergency": "integer (0-50)",
  "number_inpatient": "integer (0-50)",
  "diag_1": "string (ICD-9 code)",
  "diag_2": "string (ICD-9 code, optional)",
  "diag_3": "string (ICD-9 code, optional)",
  "number_diagnoses": "integer (1-20)",
  "max_glu_serum": "string (>200/<=200/None)",
  "A1Cresult": "string (>7/<=7/None)",
  "metformin": "string (Yes/No/Steady/Up/Down)",
  "repaglinide": "string (Yes/No/Steady/Up/Down)",
  "nateglinide": "string (Yes/No/Steady/Up/Down)",
  "chlorpropamide": "string (Yes/No/Steady/Up/Down)",
  "glimepiride": "string (Yes/No/Steady/Up/Down)",
  "acetohexamide": "string (Yes/No/Steady/Up/Down)",
  "glipizide": "string (Yes/No/Steady/Up/Down)",
  "glyburide": "string (Yes/No/Steady/Up/Down)",
  "tolbutamide": "string (Yes/No/Steady/Up/Down)",
  "pioglitazone": "string (Yes/No/Steady/Up/Down)",
  "rosiglitazone": "string (Yes/No/Steady/Up/Down)",
  "acarbose": "string (Yes/No/Steady/Up/Down)",
  "miglitol": "string (Yes/No/Steady/Up/Down)",
  "troglitazone": "string (Yes/No/Steady/Up/Down)",
  "tolazamide": "string (Yes/No/Steady/Up/Down)",
  "examide": "string (Yes/No/Steady/Up/Down)",
  "citoglipton": "string (Yes/No/Steady/Up/Down)",
  "insulin": "string (Yes/No/Steady/Up/Down)",
  "glyburide-metformin": "string (Yes/No/Steady/Up/Down)",
  "glipizide-metformin": "string (Yes/No/Steady/Up/Down)",
  "glimepiride-pioglitazone": "string (Yes/No/Steady/Up/Down)",
  "metformin-rosiglitazone": "string (Yes/No/Steady/Up/Down)",
  "metformin-pioglitazone": "string (Yes/No/Steady/Up/Down)",
  "change": "string (Yes/No/Ch)",
  "diabetesMed": "string (Yes/No)",
  "readmitted": "string (Yes/No, optional for predictions)"
}
```

---

## 🚨 ERROR HANDLING

### **HTTP Status Codes**
- `200 OK` - Successful prediction
- `400 Bad Request` - Invalid input data
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server-side errors
- `503 Service Unavailable` - Service temporarily unavailable

### **Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid patient data provided",
    "details": [
      {
        "field": "age",
        "issue": "Age must be between 1 and 100",
        "value": 150
      }
    ],
    "timestamp": "2025-08-19T18:42:56.143056",
    "request_id": "req_12345"
  }
}
```

### **Common Error Codes**
- `VALIDATION_ERROR` - Input data validation failed
- `MODEL_LOAD_ERROR` - ML model failed to load
- `PREDICTION_ERROR` - Model prediction failed
- `SERVICE_UNAVAILABLE` - Service temporarily unavailable
- `RATE_LIMIT_EXCEEDED` - Too many requests

---

## 📈 PERFORMANCE & LIMITS

### **Performance Metrics**
- **Response Time:** <100ms (95th percentile)
- **Throughput:** 1000+ requests/second
- **Uptime:** >99.9%
- **Model Accuracy:** 93.12%

### **Rate Limits**
- **Single Predictions:** 100 requests/minute
- **Batch Predictions:** 10 requests/minute
- **Health Checks:** 1000 requests/minute

### **Payload Limits**
- **Single Prediction:** 1MB
- **Batch Prediction:** 10MB
- **Max Patients per Batch:** 100

---

## 🔐 AUTHENTICATION & SECURITY

### **Current Status:**
- **Authentication:** Not required (development phase)
- **HTTPS:** Enabled (TLS 1.3)
- **Data Encryption:** At rest and in transit
- **Audit Logging:** Full request/response logging

### **Future Security Features:**
- **API Key Authentication**
- **JWT Token Support**
- **Role-Based Access Control**
- **IP Whitelisting**

---

## 📊 MONITORING & METRICS

### **Available Metrics**
- Request/response times
- Error rates and types
- Model performance metrics
- Resource utilization
- User activity patterns

### **Monitoring Tools**
- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboard
- **Azure Monitor** - Cloud monitoring
- **Custom Health Checks** - Application monitoring

---

## 🚀 DEPLOYMENT & SCALING

### **Current Deployment**
- **Platform:** Azure Container Apps
- **Region:** East US
- **Scaling:** Auto-scaling enabled
- **Replicas:** 2-10 (based on load)

### **Scaling Behavior**
- **Scale Up:** CPU >70% or memory >80%
- **Scale Down:** CPU <30% and memory <40%
- **Cooldown:** 5 minutes between scaling events

---

## 📚 ADDITIONAL RESOURCES

### **Interactive Documentation**
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`
- **OpenAPI Schema:** `/openapi.json`

### **Code Examples**
- **Python Client:** Available in `/examples/python_client.py`
- **JavaScript Client:** Available in `/examples/javascript_client.js`
- **cURL Examples:** Available in `/examples/curl_examples.sh`

### **Support & Contact**
- **Documentation:** This document
- **Issues:** GitHub repository issues
- **Email:** [mj.babaie@gmail.com]
- **LinkedIn:** [https://www.linkedin.com/in/mohammadbabaie/]
- **GitHub:** [https://github.com/Muh76]

---

## 📋 CHANGELOG

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-08-19 | Initial API release |
| 1.0.1 | 2025-08-19 | Added batch prediction endpoint |
| 1.0.2 | 2025-08-19 | Enhanced error handling |

---

**API Status:** 🟢 **PRODUCTION READY**
**Last Updated:** August 2025
**Next Review:** September 2025
**Contact:** Mohammad Javad Aghababaie Beni
