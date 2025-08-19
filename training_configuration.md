
# TRAINING CONFIGURATION - PHASE 2: MODEL TRAINING

## Dataset Information
- **Training Set**: 144,654 samples × 15 features
- **Test Set**: 36,164 samples × 15 features
- **Features**: encounter_id, patient_nbr, admission_type_id, admission_source_id, time_in_hospital, num_lab_procedures, num_procedures, num_medications, number_outpatient, number_emergency, number_inpatient, number_diagnoses, age_midpoint, service_utilization_score, clinical_risk_score
- **Target**: readmission_30d (binary classification)

## Model Configuration

### Baseline Models

#### Logistic Regression
- **Class**: LogisticRegression
- **Parameters**: {'random_state': 42, 'max_iter': 1000}
- **Description**: Baseline linear model for interpretability

#### Random Forest
- **Class**: RandomForestClassifier
- **Parameters**: {'n_estimators': 100, 'random_state': 42}
- **Description**: Baseline ensemble model for feature importance

### Advanced Models

#### Xgboost
- **Class**: XGBClassifier
- **Parameters**: {'random_state': 42, 'eval_metric': 'logloss'}
- **Description**: Advanced gradient boosting for performance

#### Lightgbm
- **Class**: LGBMClassifier
- **Parameters**: {'random_state': 42, 'verbose': -1}
- **Description**: Light gradient boosting for efficiency

#### Catboost
- **Class**: CatBoostClassifier
- **Parameters**: {'random_state': 42, 'verbose': False}
- **Description**: Categorical boosting for categorical features

## Interpretability Setup

### SHAP Analysis
- **Purpose**: Global and local feature importance
- **Implementation**: Post-training analysis
- **Output**: Feature importance plots and prediction explanations

### LIME Analysis
- **Purpose**: Local prediction explanations
- **Implementation**: Individual prediction analysis
- **Output**: Local feature contribution plots

## Training Workflow
1. **Baseline Models**: Train and evaluate basic models
2. **Advanced Models**: Train and evaluate advanced models
3. **Hyperparameter Optimization**: Use Optuna for tuning
4. **Model Selection**: Compare performance and select best model
5. **Interpretability Analysis**: Apply SHAP/LIME for insights
6. **Clinical Validation**: Validate results with domain experts

## Risk Mitigation
- Monitor for overfitting during training
- Validate model performance on clinical metrics
- Ensure interpretability for clinical decision support
- Document all model decisions and limitations

---
Generated on: 2025-08-19 12:51:09
Pipeline Version: 1.0
