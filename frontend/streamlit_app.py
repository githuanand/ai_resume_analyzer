import streamlit as st
import requests

# Render API URL
API_URL = "https://ai-resume-analyzer-7i3c.onrender.com/analyze/"

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: bold;
    color: #1E88E5;
    text-align: center;
}

.subtitle {
    font-size: 18px;
    text-align: center;
    color: gray;
}

.result-box {
    background-color: #f5f7fa;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<p class="big-title">🚀 AI Resume Analyzer</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Upload your Resume and get AI-powered ATS Analysis</p>',
    unsafe_allow_html=True
)

st.divider()

# Upload Resume
uploaded_file = st.file_uploader(
    "📂 Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file:

    st.success(f"Selected File: {uploaded_file.name}")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        analyze_btn = st.button(
            "🔍 Analyze Resume",
            use_container_width=True
        )

    if analyze_btn:

        with st.spinner("🤖 AI is analyzing your resume..."):

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

                    st.success("✅ Analysis Completed")

                    st.markdown("## 📊 Resume Analysis")

                    st.markdown(
                        f"""
                        <div class="result-box">
                        {result.get("analysis", "No response")}
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

st.divider()

st.markdown(
    """
    ### Features

    ✅ ATS Resume Review  
    ✅ AI/ML Job Readiness Analysis  
    ✅ Skill Gap Detection  
    ✅ Resume Improvement Suggestions  
    ✅ Powered by Groq + FastAPI + LangChain
    """
)