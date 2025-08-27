# Diabetes Readmission Prediction API Reference

**Version:** 1.0.0
**Base URL:** https://api.diabetes-readmission.com/v1

## Health Check

**Method:** GET
**Path:** /health
**Description:** Check API health and status

### Example Request
```bash
curl -X GET "https://api.diabetes-readmission.com/v1/health"
```

### Example Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 86400
}
```

## Predict Readmission

**Method:** POST
**Path:** /predict
**Description:** Predict 30-day readmission risk for a patient

### Example Request
```bash
curl -X POST "https://api.diabetes-readmission.com/v1/predict" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_data": {
      "age": 65,
      "gender": "female",
      "race": "caucasian",
      "admission_type": "emergency",
      "discharge_disposition": "home",
      "admission_source": "emergency_room",
      "time_in_hospital": 5,
      "num_lab_procedures": 45,
      "num_procedures": 2,
      "num_medications": 15,
      "number_outpatient": 3,
      "number_emergency": 1,
      "number_inpatient": 2,
      "diag_1": "250.00",
      "diag_2": "401.9",
      "diag_3": "272.4",
      "max_glu_serum": "normal",
      "a1cresult": "normal",
      "metformin": "steady",
      "repaglinide": "no",
      "nateglinide": "no",
      "chlorpropamide": "no",
      "glimepiride": "no",
      "acetohexamide": "no",
      "glipizide": "steady",
      "glyburide": "no",
      "tolbutamide": "no",
      "pioglitazone": "no",
      "rosiglitazone": "no",
      "acarbose": "no",
      "miglitol": "no",
      "troglitazone": "no",
      "tolazamide": "no",
      "examide": "no",
      "citoglipton": "no",
      "insulin": "steady",
      "glyburide_metformin": "no",
      "glipizide_metformin": "no",
      "glimepiride_pioglitazone": "no",
      "metformin_rosiglitazone": "no",
      "metformin_pioglitazone": "no",
      "change": "no",
      "diabetes_med": "yes",
      "readmitted": "no"
    }
  }'
```

### Example Response
```json
{
  "prediction": {
    "readmission_risk": 0.23,
    "risk_category": "low",
    "confidence": 0.89
  },
  "patient_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T10:30:00Z",
  "model_version": "1.0.0",
  "features_used": ["age", "time_in_hospital", "num_medications", "diag_1", "insulin"]
}
```

## Batch Predict

**Method:** POST
**Path:** /predict/batch
**Description:** Predict readmission risk for multiple patients

## Model Info

**Method:** GET
**Path:** /model/info
**Description:** Get information about the deployed model

## Model Update

**Method:** POST
**Path:** /model/update
**Description:** Update the deployed model (admin only)
