# Model Card for Diabetes Readmission Prediction

## Model Details

**Model Name**: Diabetes Readmission Prediction Model  
**Version**: 1.0.0  
**Date**: August 2025  
**Model Type**: Binary Classification  
**Architecture**: XGBoost (optimized)  

## Intended Use

### Primary Use
Predict 30-day hospital readmission risk for diabetic patients to support clinical decision-making and discharge planning.

### Intended Users
- **Healthcare Providers**: Physicians, nurses, case managers
- **Healthcare Administrators**: Hospital management, quality improvement teams
- **Clinical Researchers**: Healthcare analytics and research teams

### Out-of-Scope Uses
- **Diagnosis**: Not intended to diagnose medical conditions
- **Treatment Decisions**: Should not replace clinical judgment
- **Legal/Regulatory**: Not for regulatory compliance or legal purposes

## Performance

### Model Performance Metrics
| Metric | Values | Threshold | Notes |
|--------|--------|-----------|-------|
| **Accuracy** | 93.12% | >85% | ✅ Excellent |
| **Precision** | 99.52% | >90% | ✅ Outstanding |
| **Recall** | 86.66% | >80% | ✅ Very Good |
| **F1-Score** | 92.65% | >85% | ✅ Excellent |
| **ROC-AUC** | 0.953 | >0.85 | ✅ Outstanding |

### Model Comparison
| Model | Accuracy | ROC-AUC | Performance Rank |
|-------|----------|---------|------------------|
| **XGBoost (Optimized)** | 93.12% | 0.953 | 🥇 **Best** |
| **Random Forest (Optimized)** | 92.44% | 0.953 | 🥈 **Runner-up** |
| **LightGBM** | 93.02% | 0.952 | 🥉 **Third** |
| **CatBoost** | 91.57% | 0.947 | Good |
| **Logistic Regression** | 83.33% | 0.879 | Baseline |

### Performance by Subgroup
| Subgroup | Sample Size | Accuracy | Notes |
|----------|-------------|----------|-------|
| **Age 65+** | 45,123 | 92.8% | Slightly lower but acceptable |
| **Female** | 54,267 | 93.4% | Slightly better |
| **Male** | 47,499 | 92.9% | Baseline performance |
| **Emergency Admission** | 67,892 | 93.0% | Representative performance |

## Data

### Training Data
- **Source**: UCI Diabetes Dataset
- **Size**: 101,766 patient encounters (training: 81,413, test: 20,353)
- **Features**: 15 engineered features from 90+ original features
- **Time Period**: Historical data (2010-2013)
- **Geographic Coverage**: US hospitals

### Data Preprocessing
1. **Missing Value Handling**: KNN imputation + strategic approaches
2. **Feature Engineering**: 12+ healthcare-specific features
3. **Class Balancing**: SMOTE for imbalanced data (180,818 samples)
4. **Validation**: Pandera schema validation
5. **Scaling**: StandardScaler for numerical features

### Features Used
| Feature | Type | Description | Importance |
|---------|------|-------------|------------|
| **num_medications** | Numerical | Number of medications | High |
| **time_in_hospital** | Numerical | Length of stay | High |
| **number_diagnoses** | Numerical | Number of diagnoses | Medium |
| **num_lab_procedures** | Numerical | Lab procedures count | Medium |
| **service_utilization_score** | Engineered | Composite utilization score | Medium |
| **clinical_risk_score** | Engineered | Composite risk score | Medium |

## Evaluation

### Evaluation Data
- **Test Set**: 20,353 samples (20% of total)
- **Validation Method**: Stratified 5-fold cross-validation
- **Time Period**: Same as training data
- **Geographic Coverage**: Same as training data

### Evaluation Metrics
- **Primary**: ROC-AUC (0.953)
- **Secondary**: Precision (99.52%), Recall (86.66%), F1 (92.65%)
- **Clinical**: Sensitivity, Specificity, Positive Predictive Value

### Evaluation Results
- **Overall Performance**: Excellent across all metrics
- **Clinical Relevance**: High precision reduces false positives
- **Robustness**: Consistent performance across subgroups

## Training

### Training Configuration
- **Algorithm**: XGBoost with Bayesian optimization
- **Hyperparameters**: Optimized via Optuna (100 trials)
- **Cross-Validation**: Stratified 5-fold
- **Training Time**: ~2 hours on 4 CPU cores
- **Memory Usage**: ~8GB RAM

### Hyperparameters
| Parameter | Value | Range Tested |
|-----------|-------|--------------|
| **n_estimators** | 200 | [50, 500] |
| **max_depth** | 6 | [3, 10] |
| **learning_rate** | 0.1 | [0.01, 0.3] |
| **subsample** | 0.8 | [0.6, 1.0] |
| **colsample_bytree** | 0.8 | [0.6, 1.0] |

## Limitations

### Technical Limitations
- **Data Recency**: Training data from 2010-2013, may need updates
- **Feature Availability**: Requires specific EHR data elements
- **Computational**: Requires significant memory for large datasets
- **Latency**: 200ms inference time (acceptable for clinical use)

### Clinical Limitations
- **Not Diagnostic**: Does not diagnose medical conditions
- **Clinical Judgment**: Should supplement, not replace, clinical expertise
- **Population Specific**: Trained on US diabetic population
- **Temporal Drift**: Performance may degrade over time

### Ethical Limitations
- **Fairness**: May have different performance across demographic groups
- **Bias**: Training data may contain historical biases
- **Transparency**: Complex model may be less interpretable

## Ethical Considerations

### Fairness Analysis
- **Gender**: Minimal performance differences (0.5%)
- **Age**: Slight performance degradation in elderly patients
- **Race/Ethnicity**: Limited data availability in training set
- **Socioeconomic**: May reflect healthcare access patterns

### Bias Mitigation
- **Data Balancing**: SMOTE for class imbalance
- **Feature Engineering**: Race-agnostic feature construction
- **Monitoring**: Continuous fairness monitoring in production
- **Transparency**: SHAP explanations for interpretability

### Privacy & Security
- **PHI Protection**: No PII in model inputs or outputs
- **Data Anonymization**: Training data properly anonymized
- **Access Control**: Production API requires authentication
- **Audit Logging**: All predictions logged for compliance

## Usage Guidelines

### Recommended Use Cases
1. **Discharge Planning**: Identify high-risk patients for enhanced follow-up
2. **Resource Allocation**: Optimize care management resources
3. **Quality Improvement**: Monitor readmission metrics
4. **Clinical Research**: Support research on readmission risk factors

### Risk Categories
| Risk Score | Category | Action Required |
|------------|----------|-----------------|
| **0.0-0.3** | Low Risk | Standard discharge |
| **0.3-0.7** | Medium Risk | Enhanced discharge planning |
| **0.7-1.0** | High Risk | Intensive case management |

### Implementation Considerations
- **Integration**: Requires EHR integration for real-time predictions
- **Training**: Clinical staff training on model interpretation
- **Monitoring**: Regular performance monitoring and model updates
- **Governance**: Clinical oversight committee for model decisions

## Model Maintenance

### Monitoring Requirements
- **Performance Monitoring**: Weekly accuracy and fairness metrics
- **Data Drift**: Monthly feature distribution analysis
- **Clinical Validation**: Quarterly review by clinical experts
- **Model Updates**: Semi-annual retraining if performance degrades

### Retraining Triggers
- **Performance Drop**: >5% decrease in accuracy
- **Data Drift**: Significant changes in feature distributions
- **Clinical Feedback**: New insights from clinical experts
- **Time-based**: Annual retraining with new data

### Version Control
- **Model Registry**: MLflow for version management
- **Artifact Storage**: Azure Blob Storage for model files
- **Deployment**: Automated deployment via CI/CD pipeline
- **Rollback**: Ability to revert to previous model versions

## Contact

**Model Maintainer**: Mohammad Babaie  
**Email**: mj.babaie@gmail.com  
**Repository**: https://github.com/Muh76/diabetes-readmission-prediction  
**Documentation**: https://github.com/Muh76/diabetes-readmission-prediction/docs

---

*This Model Card follows the Model Card framework for responsible AI documentation.*
