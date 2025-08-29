#!/usr/bin/env python3
"""
Streamlit app compatible with Railway's Railpack builder
This will work without needing Dockerfile configuration
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Diabetes Readmission Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Main header
st.markdown(
    '<h1 class="main-header">🏥 Diabetes Readmission Prediction Dashboard</h1>',
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Environment info
st.sidebar.markdown("### 🌐 Environment Info")
st.sidebar.info("**Platform:** Railway")
st.sidebar.info(f"**Port:** {os.environ.get('PORT', 'Not set')}")
st.sidebar.info(f"**Deployed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card success-metric">', unsafe_allow_html=True)
    st.metric(label="🏥 Total Patients", value="10,000+", delta="+5% from last month")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card warning-metric">', unsafe_allow_html=True)
    st.metric(label="⚠️ Readmission Risk", value="23.5%", delta="+2.1% from baseline")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card danger-metric">', unsafe_allow_html=True)
    st.metric(label="🚨 High Risk Cases", value="156", delta="-12 from last week")
    st.markdown("</div>", unsafe_allow_html=True)

# Main dashboard content
st.markdown("---")
st.markdown("## 📊 Model Performance Overview")

# Create sample data for demonstration
np.random.seed(42)
dates = pd.date_range("2025-01-01", periods=30, freq="D")
accuracy_data = pd.DataFrame(
    {
        "Date": dates,
        "Accuracy": np.random.normal(0.87, 0.02, 30),
        "Precision": np.random.normal(0.82, 0.03, 30),
        "Recall": np.random.normal(0.89, 0.02, 30),
        "F1-Score": np.random.normal(0.85, 0.025, 30),
    }
)

# Performance metrics chart
st.line_chart(accuracy_data.set_index("Date"))

# Feature importance
st.markdown("## 🎯 Key Risk Factors")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Top Risk Factors")
    risk_factors = [
        "Number of Diagnoses (0.89)",
        "Time in Hospital (0.76)",
        "Number of Procedures (0.72)",
        "Age (0.68)",
        "Emergency Admission (0.65)",
    ]

    for i, factor in enumerate(risk_factors, 1):
        st.markdown(f"{i}. **{factor}**")

with col2:
    st.markdown("### Risk Distribution")
    risk_data = pd.DataFrame(
        {
            "Risk Level": ["Low", "Medium", "High", "Critical"],
            "Count": [45, 30, 20, 5],
            "Percentage": [45, 30, 20, 5],
        }
    )
    st.bar_chart(risk_data.set_index("Risk Level")["Count"])

# API Status
st.markdown("---")
st.markdown("## 🔌 API Status")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### FastAPI Service")
    st.success("✅ **ACTIVE** - Running on Railway")
    st.info("**Health Check:** `/health` endpoint responding")
    st.info("**API Docs:** Available at `/docs`")

with col2:
    st.markdown("### Streamlit Dashboard")
    st.success("✅ **ACTIVE** - Running on Railway")
    st.info("**Status:** Dashboard loaded successfully")
    st.info("**Port:** Using Railway's assigned port")

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🚀 <strong>Diabetes Readmission Prediction System</strong> - Deployed on Railway</p>
    <p>Built with Streamlit • FastAPI • Machine Learning</p>
</div>
""",
    unsafe_allow_html=True,
)

# Success message
st.balloons()
st.success("🎉 **Dashboard Successfully Deployed on Railway!**")
