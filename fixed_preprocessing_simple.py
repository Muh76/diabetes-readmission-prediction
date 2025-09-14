
def preprocess_features(patient_data: PatientData) -> np.ndarray:
    """Simple preprocessing that matches training pipeline"""
    try:
        # Convert to DataFrame
        data_dict = patient_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Create feature vector with exact same order as training
        features = np.zeros(305, dtype=np.float32)
        
        # Map core numerical features (these are the most important)
        core_features = {
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
            'number_diagnoses': 12
        }
        
        # Map core features
        for feature_name, idx in core_features.items():
            if feature_name in data_dict and data_dict[feature_name] is not None:
                features[idx] = float(data_dict[feature_name])
        
        # Map engineered features (these are crucial for different predictions)
        engineered_features = {
            'clinical_risk': 13,
            'treatment_complexity': 14,
            'socioeconomic_risk': 15,
            'medication_adherence': 16,
            'hospital_utilization': 17,
            'lab_efficiency': 18,
            'los_risk': 19,
            'diagnosis_complexity': 20,
            'clinical_severity': 22,
            'medication_complexity': 23,
            'clinical_risk_score': 24,
            'comorbidity_count': 26,
            'comorbidity_severity': 27,
            'procedure_intensity': 28
        }
        
        # Map engineered features
        for feature_name, idx in engineered_features.items():
            if feature_name in data_dict and data_dict[feature_name] is not None:
                features[idx] = float(data_dict[feature_name])
        
        # Map categorical features (simplified)
        categorical_mappings = {
            'race': {'Caucasian': 42, 'AfricanAmerican': 43, 'Hispanic': 44, 'Asian': 45, 'Other': 46},
            'gender': {'Female': 47, 'Male': 48},
            'age': {'[0-10)': 49, '[10-20)': 50, '[20-30)': 51, '[30-40)': 52, '[40-50)': 53, 
                   '[50-60)': 54, '[60-70)': 55, '[70-80)': 56, '[80-90)': 57, '[90-100)': 58},
            'weight': {'?': 59, '[0-25)': 60, '[25-50)': 61, '[50-75)': 62, '[75-100)': 63, 
                      '[100-125)': 64, '[125-150)': 65, '[150-175)': 66, '[175-200)': 67, 
                      '>200': 68}
        }
        
        # Map categorical features
        for cat_feature, mapping in categorical_mappings.items():
            if cat_feature in data_dict and data_dict[cat_feature] is not None:
                value = data_dict[cat_feature]
                if value in mapping:
                    features[mapping[value]] = 1.0
        
        # Map medication features (these are important for predictions)
        medication_features = {
            'metformin': 305, 'insulin': 322, 'glipizide': 311, 'glyburide': 312,
            'pioglitazone': 314, 'rosiglitazone': 315, 'acarbose': 316,
            'miglitol': 317, 'troglitazone': 318, 'tolazamide': 319,
            'citoglipton': 321, 'change': 328, 'diabetesMed': 329
        }
        
        for med_feature, idx in medication_features.items():
            if med_feature in data_dict and data_dict[med_feature] is not None:
                value = data_dict[med_feature]
                if value in ['Up', 'Down', 'Steady', 'Ch']:
                    features[idx] = 1.0
        
        # Ensure we have exactly 305 features
        if len(features) != 305:
            features = np.resize(features, 305)
        
        # Scale features if scaler is available
        if scaler is not None:
            features = scaler.transform(features.reshape(1, -1)).flatten()
            
        return features.reshape(1, -1)
        
    except Exception as e:
        logger.error(f"Error preprocessing features: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Feature preprocessing failed: {str(e)}")
