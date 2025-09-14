
# Proper feature mapping for API
FEATURE_MAPPING = {
    # Numerical features (first 42)
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

# Categorical mappings (one-hot encoded)
CATEGORICAL_MAPPINGS = {
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

# Medication features (binary)
MEDICATION_FEATURES = {
    'metformin': 305, 'repaglinide': 306, 'nateglinide': 307, 'chlorpropamide': 308,
    'glimepiride': 309, 'acetohexamide': 310, 'glipizide': 311, 'glyburide': 312,
    'tolbutamide': 313, 'pioglitazone': 314, 'rosiglitazone': 315, 'acarbose': 316,
    'miglitol': 317, 'troglitazone': 318, 'tolazamide': 319, 'examide': 320,
    'citoglipton': 321, 'insulin': 322, 'glyburide_metformin': 323,
    'glipizide_metformin': 324, 'glimepiride_pioglitazone': 325,
    'metformin_rosiglitazone': 326, 'metformin_pioglitazone': 327,
    'change': 328, 'diabetesMed': 329
}
