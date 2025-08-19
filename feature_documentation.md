
# FEATURE DOCUMENTATION - DIABETIC READMISSION PREDICTION

## Feature Overview
This document describes all features used in the diabetic readmission prediction model.

## Feature Details

### encounter_id
- **Description**: Unique identifier for each hospital encounter
- **Type**: float64
- **Range**: -1.05 to 2.05

### patient_nbr
- **Description**: Unique identifier for each patient
- **Type**: float64
- **Range**: -0.71 to 2.24

### admission_type_id
- **Description**: Type of admission (1=Emergency, 2=Elective, etc.)
- **Type**: float64
- **Range**: 0.00 to 7.00

### admission_source_id
- **Description**: Source of admission (1=Physician referral, 2=Clinic referral, etc.)
- **Type**: float64
- **Range**: -1.20 to 3.60

### time_in_hospital
- **Description**: Number of days between admission and discharge
- **Type**: float64
- **Range**: -0.75 to 2.50

### num_lab_procedures
- **Description**: Number of laboratory procedures performed
- **Type**: float64
- **Range**: -1.87 to 3.74

### num_procedures
- **Description**: Number of procedures performed
- **Type**: float64
- **Range**: -0.50 to 2.50

### num_medications
- **Description**: Number of distinct medications administered
- **Type**: float64
- **Range**: -1.56 to 7.33

### number_outpatient
- **Description**: Number of outpatient visits in the year preceding admission
- **Type**: float64
- **Range**: 0.00 to 40.00

### number_emergency
- **Description**: Number of emergency visits in the year preceding admission
- **Type**: float64
- **Range**: 0.00 to 76.00

### number_inpatient
- **Description**: Number of inpatient visits in the year preceding admission
- **Type**: float64
- **Range**: 0.00 to 21.00

### number_diagnoses
- **Description**: Number of diagnoses entered in the system
- **Type**: float64
- **Range**: -2.33 to 2.67

### age_midpoint
- **Description**: Age group midpoint (derived from age ranges)
- **Type**: float64
- **Range**: -3.00 to 1.50

### service_utilization_score
- **Description**: Weighted score of outpatient, emergency, and inpatient visits
- **Type**: float64
- **Range**: -0.49 to 51.08

### clinical_risk_score
- **Description**: Composite risk score based on procedures, lab tests, diagnoses, and medications
- **Type**: float64
- **Range**: -1.17 to 1.50


## Clinical Validation Notes
- **Temporal Integrity**: All features are pre-discharge (no post-discharge information)
- **Feature Engineering**: Some features are derived from original clinical data
- **Interpretability**: Features designed for clinical relevance and model interpretability

## Usage Guidelines
- Use this documentation for clinical validation
- Consult with healthcare experts for feature interpretation
- Monitor feature importance during model training
- Validate feature ranges against clinical standards

---
Generated on: 2025-08-19 12:49:58
Pipeline Version: 1.0
