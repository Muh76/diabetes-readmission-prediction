# API Schema Documentation

## Prediction Request Schema

### Input Model (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import Optional

class PatientData(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    gender: str = Field(..., description="Patient gender (Male/Female)")
    admission_type_id: int = Field(..., description="Type of admission")
    discharge_disposition_id: int = Field(..., description="Discharge disposition")
    admission_source_id: int = Field(..., description="Source of admission")
    time_in_hospital: int = Field(..., ge=1, le=365, description="Length of stay in days")
    num_lab_procedures: int = Field(..., ge=0, description="Number of lab procedures")
    num_procedures: int = Field(..., ge=0, description="Number of procedures")
    num_medications: int = Field(..., ge=0, description="Number of medications")
    number_outpatient: int = Field(..., ge=0, description="Number of outpatient visits")
    number_emergency: int = Field(..., ge=0, description="Number of emergency visits")
    number_inpatient: int = Field(..., ge=0, description="Number of inpatient visits")
    diag_1: str = Field(..., description="Primary diagnosis code")
    diag_2: Optional[str] = Field(None, description="Secondary diagnosis code")
    diag_3: Optional[str] = Field(None, description="Tertiary diagnosis code")
    max_glu_serum: str = Field(..., description="Maximum glucose serum result")
    A1Cresult: str = Field(..., description="A1C test result")
    metformin: str = Field(..., description="Metformin medication status")
    repaglinide: str = Field(..., description="Repaglinide medication status")
    nateglinide: str = Field(..., description="Nateglinide medication status")
    chlorpropamide: str = Field(..., description="Chlorpropamide medication status")
    glimepiride: str = Field(..., description="Glimepiride medication status")
    acetohexamide: str = Field(..., description="Acetohexamide medication status")
    glipizide: str = Field(..., description="Glipizide medication status")
    glyburide: str = Field(..., description="Glyburide medication status")
    tolbutamide: str = Field(..., description="Tolbutamide medication status")
    pioglitazone: str = Field(..., description="Pioglitazone medication status")
    rosiglitazone: str = Field(..., description="Rosiglitazone medication status")
    acarbose: str = Field(..., description="Acarbose medication status")
    miglitol: str = Field(..., description="Miglitol medication status")
    troglitazone: str = Field(..., description="Troglitazone medication status")
    tolazamide: str = Field(..., description="Tolazamide medication status")
    examide: str = Field(..., description="Examide medication status")
    citoglipton: str = Field(..., description="Citoglipton medication status")
    insulin: str = Field(..., description="Insulin medication status")
    glyburide_metformin: str = Field(..., description="Glyburide-metformin combination")
    glipizide_metformin: str = Field(..., description="Glipizide-metformin combination")
    glimepiride_pioglitazone: str = Field(..., description="Glimepiride-pioglitazone combination")
    metformin_rosiglitazone: str = Field(..., description="Metformin-rosiglitazone combination")
    metformin_pioglitazone: str = Field(..., description="Metformin-pioglitazone combination")
    change: str = Field(..., description="Change in diabetes medications")
    diabetesMed: str = Field(..., description="Diabetes medication prescribed")

class PredictionRequest(BaseModel):
    patient_data: PatientData
```

### Response Model (Pydantic)

```python
class PredictionResponse(BaseModel):
    prediction: dict = Field(..., description="Prediction results")
    patient_id: str = Field(..., description="Patient identifier")
    model_version: str = Field(..., description="Model version used")
    timestamp: str = Field(..., description="Prediction timestamp")
    confidence: float = Field(..., description="Prediction confidence score")
    risk_factors: list = Field(..., description="Top risk factors")
```

## Important Notes

### Prediction Timing
- **Model predicts at DISCHARGE time**
- Features like `discharge_disposition_id` are only known at discharge
- This prevents data leakage and ensures realistic deployment

### Data Validation
- All features are validated using Pydantic schemas
- Missing values are handled appropriately
- Out-of-range values are rejected with clear error messages

### Security
- No PHI is logged or stored
- All requests are anonymized
- Audit logging for compliance

## Example Usage

### Single Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "patient_data": {
         "patient_id": "test_001",
         "age": 65,
         "gender": "Female",
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
         "diag_1": "250.00",
         "diag_2": "250.00",
         "diag_3": "250.00",
         "max_glu_serum": "None",
         "A1Cresult": "None",
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
         "glyburide_metformin": "No",
         "glipizide_metformin": "No",
         "glimepiride_pioglitazone": "No",
         "metformin_rosiglitazone": "No",
         "metformin_pioglitazone": "No",
         "change": "No",
         "diabetesMed": "No"
       }
     }'
```

### Expected Response
```json
{
  "prediction": {
    "readmission_risk": 0.23,
    "risk_category": "low",
    "confidence": 0.89
  },
  "patient_id": "test_001",
  "model_version": "1.0.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "confidence": 0.89,
  "risk_factors": [
    "num_medications: 0.18",
    "time_in_hospital: 0.15",
    "number_diagnoses: 0.12"
  ]
}
```

## Error Handling

### Validation Errors
```json
{
  "detail": [
    {
      "loc": ["body", "patient_data", "age"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt",
      "ctx": {"limit_value": 0}
    }
  ]
}
```

### Model Errors
```json
{
  "detail": "Model prediction failed. Please check input data and try again."
}
```

## API Endpoints

- **POST /predict**: Single patient prediction
- **POST /predict/batch**: Batch predictions (up to 100 patients)
- **GET /health**: Health check endpoint
- **GET /model/info**: Model information and metadata
- **GET /docs**: Interactive API documentation (Swagger UI)
