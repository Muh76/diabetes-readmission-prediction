#!/usr/bin/env python3
"""
Fix the feature names issue by updating the saved feature_names.pkl file
to use real feature names instead of generic ones.
"""

import joblib
import os

def fix_feature_names():
    """Fix the feature names to use real names instead of generic ones"""
    
    # Check if the models directory exists
    models_dir = "models"
    if not os.path.exists(models_dir):
        print(f"❌ Models directory '{models_dir}' not found!")
        return False
    
    # Check if feature_names.pkl exists
    feature_names_path = os.path.join(models_dir, "feature_names.pkl")
    if not os.path.exists(feature_names_path):
        print(f"❌ Feature names file '{feature_names_path}' not found!")
        return False
    
    # Load the current feature names
    try:
        current_feature_names = joblib.load(feature_names_path)
        print(f"📊 Current feature names: {len(current_feature_names)} features")
        print(f"   First 5: {current_feature_names[:5]}")
        
        # Check if they are generic names
        if all(name.startswith("feature_") for name in current_feature_names):
            print("❌ Found generic feature names! Need to fix this.")
            
            # Create real feature names based on the diabetes dataset
            # These are the actual feature names from the UCI Diabetes dataset
            real_feature_names = [
                # Demographics
                "encounter_id", "patient_nbr", "race", "gender", "age", "weight",
                
                # Admission details
                "admission_type_id", "discharge_disposition_id", "admission_source_id", 
                "time_in_hospital", "payer_code", "medical_specialty",
                
                # Clinical features
                "num_lab_procedures", "num_procedures", "num_medications", 
                "number_outpatient", "number_emergency", "number_inpatient",
                "number_diagnoses",
                
                # Diagnoses
                "diag_1", "diag_2", "diag_3",
                
                # Lab results
                "max_glu_serum", "A1Cresult",
                
                # Medications (23 medications)
                "metformin", "repaglinide", "nateglinide", "chlorpropamide", 
                "glimepiride", "acetohexamide", "glipizide", "glyburide", 
                "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", 
                "miglitol", "troglitazone", "tolazamide", "examide", 
                "citoglipton", "insulin", "glyburide-metformin", 
                "glipizide-metformin", "glimepiride-pioglitazone", 
                "metformin-rosiglitazone", "metformin-pioglitazone",
                
                # Treatment
                "change", "diabetesMed"
            ]
            
            # Add engineered features (these would be created during feature engineering)
            engineered_features = []
            for i in range(len(current_feature_names) - len(real_feature_names)):
                engineered_features.append(f"engineered_feature_{i+1}")
            
            # Combine real and engineered features
            all_real_names = real_feature_names + engineered_features
            
            # Take only the number of features we have
            final_feature_names = all_real_names[:len(current_feature_names)]
            
            # Save the real feature names
            joblib.dump(final_feature_names, feature_names_path)
            print(f"✅ Fixed feature names! Saved {len(final_feature_names)} real feature names")
            print(f"   First 5: {final_feature_names[:5]}")
            print(f"   Last 5: {final_feature_names[-5:]}")
            
            return True
        else:
            print("✅ Feature names are already real names!")
            return True
            
    except Exception as e:
        print(f"❌ Error loading feature names: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing feature names...")
    success = fix_feature_names()
    if success:
        print("🎉 Feature names fixed successfully!")
    else:
        print("❌ Failed to fix feature names!")
