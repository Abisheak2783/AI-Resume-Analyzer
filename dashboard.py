import streamlit as st


def dashboard_page():

    st.title("🏠 Dashboard")

    st.success("Welcome to AI Resume Analyzer")

    # ==============================
    # Dashboard Metrics
    # ==============================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("ATS Score", "92%")

    with col2:
        st.metric("Resume Match", "88%")

    with col3:
        st.metric("Missing Skills", "5")

    with col4:
        st.metric("Status", "Excellent")

    st.markdown("---")

    st.subheader("📊 Dashboard Overview")

    st.info("""
This dashboard gives a quick overview of your resume performance.

You can use the sidebar to access:

- 📄 Resume Analysis
- 📊 ATS Score
- 🎯 Resume Matching
- 🧠 Interview Coach
- 💼 Career Advisor
- 📥 Reports
""")