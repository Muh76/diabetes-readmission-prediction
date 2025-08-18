#!/usr/bin/env python3
"""
Power BI Data Preparation Script
Diabetes Readmission Prediction Project

This script prepares the cleaned and engineered dataset for Power BI dashboard creation.
It exports data in formats optimized for Power BI and creates calculated fields.
"""

import warnings

import pandas as pd

warnings.filterwarnings("ignore")


def load_and_prepare_data():
    """Load the diabetic dataset and apply all feature engineering"""
    print("🔄 Loading and preparing data for Power BI...")

    # Load the dataset
    df = pd.read_csv("diabetic_data.csv")
    print(f"✅ Loaded {len(df):,} patient records with {len(df.columns)} features")

    return df


def create_powerbi_features(df):
    """Create all the engineered features for Power BI dashboard"""
    print("🔧 Creating Power BI optimized features...")

    # 1. Target Variable Creation
    df["readmission_30d"] = (df["readmitted"] == "<30").astype(int)
    df["readmission_status"] = df["readmitted"].map(
        {
            "NO": "No Readmission",
            ">30": "Readmission >30 days",
            "<30": "Readmission <30 days",
        }
    )

    # 2. Clinical Risk Stratification
    df["clinical_risk"] = pd.cut(
        df["number_diagnoses"],
        bins=[0, 3, 6, 10, 100],
        labels=["Low", "Medium", "High", "Critical"],
    )

    # 3. Treatment Complexity Analysis
    df["treatment_complexity"] = (
        df["num_procedures"] * 0.3
        + df["num_medications"] * 0.4
        + df["number_diagnoses"] * 0.3
    )

    df["complexity_level"] = pd.cut(
        df["treatment_complexity"],
        bins=[0, 5, 10, 15, 100],
        labels=["Low", "Medium", "High", "Critical"],
    )

    # 4. Socioeconomic Risk Assessment
    def calculate_socioeconomic_risk(row):
        risk_score = 0
        if row["payer_code"] == "MC":  # Medicaid
            risk_score += 2
        elif row["payer_code"] == "MD":  # Medicare
            risk_score += 1
        if row["race"] == "AfricanAmerican":
            risk_score += 1
        if row["age"] == "?":
            risk_score += 1
        if row["weight"] == "?":
            risk_score += 1
        return risk_score

    df["socioeconomic_risk_score"] = df.apply(calculate_socioeconomic_risk, axis=1)
    df["socioeconomic_risk"] = pd.cut(
        df["socioeconomic_risk_score"],
        bins=[0, 1, 2, 3, 10],
        labels=["Low", "Medium", "High", "Critical"],
    )

    # 5. Advanced Feature Engineering
    # Age Group Categorization
    def categorize_age(age_str):
        if age_str == "?":
            return "Unknown"
        try:
            # Handle string ranges like "[0-10)"
            if "[" in age_str and ")" in age_str:
                age_range = age_str.strip("[]()").split("-")
                if len(age_range) == 2:
                    start_age = int(age_range[0])
                    if start_age < 30:
                        return "Young"
                    elif start_age < 50:
                        return "Middle"
                    elif start_age < 70:
                        return "Senior"
                    else:
                        return "Elderly"
        except (ValueError, IndexError):
            pass
        return "Unknown"

    df["age_group"] = df["age"].apply(categorize_age)

    # Length of Stay Risk
    df["los_risk"] = pd.cut(
        df["time_in_hospital"],
        bins=[0, 3, 7, 14, 100],
        labels=["Low", "Medium", "High", "Critical"],
    )

    # Clinical Severity Index
    df["clinical_severity"] = (
        df["number_diagnoses"] * 0.3
        + df["num_procedures"] * 0.2
        + df["num_medications"] * 0.2
        + df["time_in_hospital"] * 0.3
    )

    df["severity_level"] = pd.cut(
        df["clinical_severity"],
        bins=[0, 5, 10, 15, 100],
        labels=["Mild", "Moderate", "Severe", "Critical"],
    )

    # 6. Additional Power BI Optimized Features
    # Insurance Type Categories
    df["insurance_category"] = (
        df["payer_code"]
        .map(
            {
                "MC": "Medicaid",
                "MD": "Medicare",
                "HM": "Health Maintenance Organization",
                "SP": "Self Pay",
                "CP": "Commercial Insurance",
                "SI": "State Insurance",
                "CM": "Commercial Insurance",
                "UN": "Unknown",
                "DM": "Disability",
                "BC": "Blue Cross",
                "OG": "Other Government",
            }
        )
        .fillna("Other")
    )

    # Race Categories
    df["race_category"] = (
        df["race"]
        .map(
            {
                "Caucasian": "White",
                "AfricanAmerican": "Black",
                "Hispanic": "Hispanic",
                "Asian": "Asian",
                "Other": "Other",
            }
        )
        .fillna("Unknown")
    )

    # Gender Categories
    df["gender_category"] = (
        df["gender"]
        .map({"Male": "Male", "Female": "Female", "Unknown/Invalid": "Unknown"})
        .fillna("Unknown")
    )

    print("✅ All Power BI features created successfully")
    return df


def create_powerbi_calculations(df):
    """Create calculated fields and KPIs for Power BI"""
    print("📊 Creating Power BI calculations and KPIs...")

    # Calculate key metrics
    total_patients = len(df)
    readmission_rate = df["readmission_30d"].mean() * 100

    # Risk-based metrics
    high_risk_patients = len(df[df["clinical_risk"].isin(["High", "Critical"])])
    high_risk_readmission_rate = (
        df[df["clinical_risk"].isin(["High", "Critical"])]["readmission_30d"].mean()
        * 100
    )

    # Complexity metrics
    critical_complexity = len(df[df["complexity_level"] == "Critical"])
    critical_readmission_rate = (
        df[df["complexity_level"] == "Critical"]["readmission_30d"].mean() * 100
    )

    # Socioeconomic metrics
    high_socioeconomic_risk = len(
        df[df["socioeconomic_risk"].isin(["High", "Critical"])]
    )
    high_socioeconomic_readmission_rate = (
        df[df["socioeconomic_risk"].isin(["High", "Critical"])][
            "readmission_30d"
        ].mean()
        * 100
    )

    # Create summary dataframe
    summary_metrics = pd.DataFrame(
        {
            "Metric": [
                "Total Patients",
                "Overall Readmission Rate (%)",
                "High Risk Patients",
                "High Risk Readmission Rate (%)",
                "Critical Complexity Patients",
                "Critical Complexity Readmission Rate (%)",
                "High Socioeconomic Risk Patients",
                "High Socioeconomic Risk Readmission Rate (%)",
            ],
            "Value": [
                total_patients,
                round(readmission_rate, 2),
                high_risk_patients,
                round(high_risk_readmission_rate, 2),
                critical_complexity,
                round(critical_readmission_rate, 2),
                high_socioeconomic_risk,
                round(high_socioeconomic_readmission_rate, 2),
            ],
        }
    )

    print("✅ Power BI calculations and KPIs created")
    return summary_metrics


def export_for_powerbi(df, summary_metrics):
    """Export data in formats optimized for Power BI"""
    print("📤 Exporting data for Power BI...")

    # 1. Main dataset (CSV format - Power BI preferred)
    df.to_csv("powerbi_main_dataset.csv", index=False)
    print("✅ Exported main dataset: powerbi_main_dataset.csv")

    # 2. Summary metrics (CSV format)
    summary_metrics.to_csv("powerbi_summary_metrics.csv", index=False)
    print("✅ Exported summary metrics: powerbi_summary_metrics.csv")

    # 3. Risk analysis tables
    # Clinical risk analysis
    clinical_risk_analysis = (
        df.groupby("clinical_risk")
        .agg(
            {
                "readmission_30d": ["count", "mean"],
                "time_in_hospital": "mean",
                "num_medications": "mean",
            }
        )
        .round(3)
    )
    clinical_risk_analysis.columns = [
        "Patient_Count",
        "Readmission_Rate",
        "Avg_LOS",
        "Avg_Medications",
    ]
    clinical_risk_analysis.to_csv("powerbi_clinical_risk_analysis.csv")
    print("✅ Exported clinical risk analysis: powerbi_clinical_risk_analysis.csv")

    # Treatment complexity analysis
    complexity_analysis = (
        df.groupby("complexity_level")
        .agg(
            {
                "readmission_30d": ["count", "mean"],
                "time_in_hospital": "mean",
                "num_procedures": "mean",
            }
        )
        .round(3)
    )
    complexity_analysis.columns = [
        "Patient_Count",
        "Readmission_Rate",
        "Avg_LOS",
        "Avg_Procedures",
    ]
    complexity_analysis.to_csv("powerbi_complexity_analysis.csv")
    print("✅ Exported complexity analysis: powerbi_complexity_analysis.csv")

    # Socioeconomic risk analysis
    socio_analysis = (
        df.groupby("socioeconomic_risk")
        .agg(
            {
                "readmission_30d": ["count", "mean"],
                "time_in_hospital": "mean",
                "insurance_category": lambda x: x.mode().iloc[0]
                if len(x.mode()) > 0
                else "Unknown",
            }
        )
        .round(3)
    )
    socio_analysis.columns = [
        "Patient_Count",
        "Readmission_Rate",
        "Avg_LOS",
        "Most_Common_Insurance",
    ]
    socio_analysis.to_csv("powerbi_socioeconomic_analysis.csv")
    print("✅ Exported socioeconomic analysis: powerbi_socioeconomic_analysis.csv")

    # Age group analysis
    age_analysis = (
        df.groupby("age_group")
        .agg(
            {
                "readmission_30d": ["count", "mean"],
                "clinical_severity": "mean",
                "treatment_complexity": "mean",
            }
        )
        .round(3)
    )
    age_analysis.columns = [
        "Patient_Count",
        "Readmission_Rate",
        "Avg_Clinical_Severity",
        "Avg_Treatment_Complexity",
    ]
    age_analysis.to_csv("powerbi_age_analysis.csv")
    print("✅ Exported age group analysis: powerbi_age_analysis.csv")

    # Insurance analysis
    insurance_analysis = (
        df.groupby("insurance_category")
        .agg(
            {
                "readmission_30d": ["count", "mean"],
                "time_in_hospital": "mean",
                "socioeconomic_risk_score": "mean",
            }
        )
        .round(3)
    )
    insurance_analysis.columns = [
        "Patient_Count",
        "Readmission_Rate",
        "Avg_LOS",
        "Avg_Socioeconomic_Risk",
    ]
    insurance_analysis.to_csv("powerbi_insurance_analysis.csv")
    print("✅ Exported insurance analysis: powerbi_insurance_analysis.csv")

    print("🎯 All Power BI data exports completed successfully!")


def create_powerbi_instructions():
    """Create instructions for Power BI dashboard creation"""
    instructions = """
# 🎯 POWER BI DASHBOARD CREATION GUIDE

## 📊 Data Files Available
1. **powerbi_main_dataset.csv** - Main dataset with all features
2. **powerbi_summary_metrics.csv** - Key performance indicators
3. **powerbi_clinical_risk_analysis.csv** - Risk stratification analysis
4. **powerbi_complexity_analysis.csv** - Treatment complexity insights
5. **powerbi_socioeconomic_analysis.csv** - Social determinants analysis
6. **powerbi_age_analysis.csv** - Age group analysis
7. **powerbi_insurance_analysis.csv** - Insurance type analysis

## 🚀 Power BI Setup Steps

### Step 1: Import Data
1. Open Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Import all CSV files
4. Set up relationships between tables

### Step 2: Create Key Visualizations

#### Dashboard 1: Executive Summary
- **KPI Cards**: Total patients, readmission rate, high-risk patients
- **Gauge Charts**: Risk distribution, complexity levels
- **Donut Charts**: Insurance distribution, age groups

#### Dashboard 2: Clinical Risk Analysis
- **Bar Charts**: Readmission rate by risk category
- **Line Charts**: Risk vs. length of stay
- **Scatter Plots**: Complexity vs. readmission rate

#### Dashboard 3: Socioeconomic Insights
- **Heat Maps**: Risk factors correlation
- **Treemaps**: Insurance type analysis
- **Funnel Charts**: Risk progression

#### Dashboard 4: Patient Demographics
- **Maps**: Geographic distribution (if available)
- **Histograms**: Age and severity distributions
- **Box Plots**: Treatment complexity by demographics

### Step 3: Advanced Features
- **Drill-through**: From summary to patient details
- **Filters**: Date ranges, risk categories, insurance types
- **Bookmarks**: Save different dashboard views
- **Tooltips**: Detailed information on hover

### Step 4: Publishing
- **Power BI Service**: Share with stakeholders
- **Embedding**: Integrate with web applications
- **Scheduling**: Automatic refresh and alerts

## 🎨 Design Recommendations
- **Color Scheme**: Healthcare blues and greens
- **Fonts**: Clear, professional typography
- **Layout**: Logical flow from summary to details
- **Interactivity**: Responsive filters and drill-downs

## 📱 Mobile Optimization
- **Responsive Design**: Adapt to different screen sizes
- **Touch-Friendly**: Large buttons and clear navigation
- **Performance**: Optimize for mobile loading

## 🔄 Maintenance
- **Data Refresh**: Set up automatic updates
- **Version Control**: Track dashboard changes
- **User Training**: Provide usage guidelines
"""

    with open("POWERBI_SETUP_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)

    print("📋 Created Power BI setup instructions: POWERBI_SETUP_INSTRUCTIONS.md")


def main():
    """Main execution function"""
    print("🚀 POWER BI DATA PREPARATION STARTED")
    print("=" * 50)

    try:
        # Load and prepare data
        df = load_and_prepare_data()

        # Create Power BI features
        df = create_powerbi_features(df)

        # Create calculations and KPIs
        summary_metrics = create_powerbi_calculations(df)

        # Export for Power BI
        export_for_powerbi(df, summary_metrics)

        # Create setup instructions
        create_powerbi_instructions()

        print("\n🎉 POWER BI DATA PREPARATION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("📁 Files created:")
        print("   • powerbi_main_dataset.csv")
        print("   • powerbi_summary_metrics.csv")
        print("   • powerbi_clinical_risk_analysis.csv")
        print("   • powerbi_complexity_analysis.csv")
        print("   • powerbi_socioeconomic_analysis.csv")
        print("   • powerbi_age_analysis.csv")
        print("   • powerbi_insurance_analysis.csv")
        print("   • POWERBI_SETUP_INSTRUCTIONS.md")
        print("\n🚀 Ready to create your Power BI dashboard!")

    except Exception as e:
        print(f"❌ Error during Power BI data preparation: {str(e)}")
        raise


if __name__ == "__main__":
    main()
