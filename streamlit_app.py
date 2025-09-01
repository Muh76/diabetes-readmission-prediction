# Streamlit Cloud Configuration
# This app is optimized for deployment on Streamlit Cloud
# Deploy at: https://share.streamlit.io

import warnings

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore")

# Page configuration
st.set_page_config(
    page_title="🏥 Diabetes Readmission Prediction Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    '<h1 class="main-header">🏥 Diabetes Readmission Prediction Dashboard</h1>',
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("---")
st.sidebar.warning("🚧 **DEMO MODE** - This is a demonstration dashboard")

# Navigation
page = st.sidebar.selectbox(
    "📱 Select Dashboard:",
    ["🏠 Home", "📊 Model Performance", "🔍 Risk Analysis", "💰 Business Impact"],
)

# Home Page
if page == "🏠 Home":
    st.markdown("## 🎯 **Welcome to the Diabetes Readmission Prediction Dashboard**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 **What This Dashboard Shows**")
        st.markdown(
            """
        - **Model Performance Metrics** - Accuracy, ROC-AUC, Precision, Recall
        - **Risk Analysis** - Patient risk stratification and factors
        - **Business Impact** - Cost savings and ROI projections
        - **Clinical Insights** - Feature importance and correlations
        """
        )

    with col2:
        st.markdown("### 🚀 **Key Features**")
        st.markdown(
            """
        - **Interactive Visualizations** - Plotly charts and graphs
        - **Real-time Updates** - Dynamic data exploration
        - **Risk Assessment** - Patient readmission probability
        - **Business Intelligence** - Financial impact analysis
        """
        )

    st.markdown("---")

    # Demo metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🎯 Model Accuracy", "93.1%", "+4.4%")

    with col2:
        st.metric("📊 ROC-AUC", "95.3%", "+17.3%")

    with col3:
        st.metric("💰 Cost Savings", "$58.8M", "+300% ROI")

    with col4:
        st.metric("🏥 Patients Analyzed", "101,766", "+15,000")

# Model Performance Page
elif page == "📊 Model Performance":
    st.markdown("## 📊 **Model Performance Metrics**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 **Overall Performance**")

        metrics_data = {
            "Metric": ["Accuracy", "ROC-AUC", "Precision", "Recall", "F1-Score"],
            "Value": [93.1, 95.3, 99.5, 86.7, 92.7],
            "Baseline": [88.7, 78.0, 88.7, 88.7, 88.7],
        }

        df_metrics = pd.DataFrame(metrics_data)
        st.dataframe(df_metrics, use_container_width=True)

    with col2:
        st.markdown("### 📈 **Performance Comparison**")

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name="Our Model",
                x=["Accuracy", "ROC-AUC", "Precision", "Recall", "F1-Score"],
                y=[93.1, 95.3, 99.5, 86.7, 92.7],
                marker_color="#1f77b4",
            )
        )

        fig.add_trace(
            go.Bar(
                name="Baseline",
                x=["Accuracy", "ROC-AUC", "Precision", "Recall", "F1-Score"],
                y=[88.7, 78.0, 88.7, 88.7, 88.7],
                marker_color="#ff7f0e",
            )
        )

        fig.update_layout(
            title="Model Performance vs Baseline",
            yaxis_title="Percentage (%)",
            barmode="group",
        )

        st.plotly_chart(fig, use_container_width=True)

# Risk Analysis Page
elif page == "🔍 Risk Analysis":
    st.markdown("## 🔍 **Patient Risk Analysis**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 **Risk Distribution**")

        risk_data = {
            "Risk Level": [
                "High Risk (>70%)",
                "Moderate Risk (40-70%)",
                "Low Risk (<40%)",
            ],
            "Percentage": [42.8, 1.34, 55.8],
        }

        df_risk = pd.DataFrame(risk_data)

        fig = px.pie(
            df_risk,
            values="Percentage",
            names="Risk Level",
            color_discrete_sequence=["#dc3545", "#ffc107", "#28a745"],
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 **Risk Factors**")

        risk_factors = {
            "Factor": [
                "Number of Medications",
                "Time in Hospital",
                "Number of Diagnoses",
                "Age",
                "Lab Procedures",
            ],
            "Importance": [0.18, 0.15, 0.12, 0.10, 0.08],
        }

        df_factors = pd.DataFrame(risk_factors)

        fig = px.bar(
            df_factors,
            x="Importance",
            y="Factor",
            orientation="h",
            color="Importance",
            color_continuous_scale="Reds",
        )

        fig.update_layout(
            title="Top Risk Factors by Importance", xaxis_title="SHAP Importance Score"
        )

        st.plotly_chart(fig, use_container_width=True)

# Business Impact Page
elif page == "💰 Business Impact":
    st.markdown("## 💰 **Business Impact & ROI Analysis**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💵 **Financial Projections**")

        financial_data = {
            "Metric": [
                "Annual Cost Savings",
                "Quality Bonus",
                "Penalty Avoidance",
                "Total Impact",
            ],
            "Value": ["$2.25M", "$1.2M", "$1.8M", "$5.25M"],
        }

        df_financial = pd.DataFrame(financial_data)
        st.dataframe(df_financial, use_container_width=True)

        st.markdown("### 📊 **ROI Analysis**")
        st.metric("Return on Investment", "300-500%", "High Impact")
        st.metric("Break-even Time", "3-4 months", "Fast Recovery")

    with col2:
        st.markdown("### 📈 **5-Year Projection**")

        years = [1, 2, 3, 4, 5]
        savings = [2.25, 4.5, 6.75, 9.0, 11.25]
        cumulative = [2.25, 6.75, 13.5, 22.5, 33.75]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=years,
                y=savings,
                mode="lines+markers",
                name="Annual Savings",
                line={"color": "#1f77b4", "width": 3},
            )
        )

        fig.add_trace(
            go.Scatter(
                x=years,
                y=cumulative,
                mode="lines+markers",
                name="Cumulative Savings",
                line={"color": "#28a745", "width": 3, "dash": "dash"},
            )
        )

        fig.update_layout(
            title="5-Year Financial Projection",
            xaxis_title="Year",
            yaxis_title="Savings (Millions $)",
        )

        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666;'>
    <p>🏥 <strong>Diabetes Readmission Prediction Dashboard</strong> | Demo Version</p>
    <p>Built with Streamlit • Powered by Machine Learning</p>
</div>
""",
    unsafe_allow_html=True,
)
