import streamlit as st
import requests

# =====================================================
# CONFIG
# =====================================================

API_URL = "https://ai-resume-analyzer-7i3c.onrender.com/analyze/"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.hero-box {
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    background: linear-gradient(135deg,#0f172a,#1e293b);
    border: 1px solid #334155;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: #60a5fa;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #cbd5e1;
}

.analysis-box {
    padding: 25px;
    border-radius: 15px;
    background-color: rgba(255,255,255,0.05);
    border: 1px solid #334155;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero-box">

<div class="hero-title">
🚀 AI Resume Analyzer
</div>

<br>

<div class="hero-subtitle">
Analyze your resume using AI-powered ATS scoring,
skill-gap detection, and career recommendations.
</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# METRICS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📄 Resume Analysis",
        value="ATS"
    )

with col2:
    st.metric(
        label="🤖 AI Model",
        value="Llama 3.1"
    )

with col3:
    st.metric(
        label="⚡ Processing",
        value="Fast"
    )

st.divider()

# =====================================================
# FEATURES
# =====================================================

st.subheader("✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
### 📊 ATS Review

Get a complete ATS compatibility analysis and score.
"""
    )

with col2:
    st.success(
        """
### 🎯 Skill Gap Detection

Identify missing skills required for your target role.
"""
    )

with col3:
    st.warning(
        """
### 🚀 AI/ML Readiness

Evaluate readiness for AI, ML, Data Science careers.
"""
    )

st.divider()

# =====================================================
# UPLOAD SECTION
# =====================================================

st.subheader("📂 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload PDF or DOCX Resume",
    type=["pdf", "docx"]
)

# =====================================================
# ANALYZE BUTTON
# =====================================================

if uploaded_file:

    st.success(
        f"Selected File: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Analyze Resume",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing Resume..."
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=180
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "✅ Analysis Completed"
                    )

                    st.subheader(
                        "📊 Analysis Report"
                    )

                    analysis = result.get(
                        "analysis",
                        "No analysis available."
                    )

                    st.markdown(
                        f"""
<div class="analysis-box">
{analysis}
</div>
""",
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">

Built with ❤️ using FastAPI • Groq • LangChain • Streamlit

</div>
""", unsafe_allow_html=True)