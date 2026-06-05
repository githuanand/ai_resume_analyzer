from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

from utils.pdf_reader import extract_text_from_pdf
from utils.docx_reader import extract_text_from_docx

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Create uploads folder if not exists
os.makedirs("uploads", exist_ok=True)

# Load Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# Home Route
@app.get("/")
async def home():

    return {
        "message": "AI Resume Analyzer Running"
    }

# Resume Analyzer Route
@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...)
):

    # Save uploaded file
    upload_path = f"uploads/{file.filename}"

    with open(upload_path, "wb") as f:
        f.write(await file.read())

    # Read Resume Text
    if file.filename.endswith(".pdf"):

        resume_text = extract_text_from_pdf(upload_path)

    elif file.filename.endswith(".docx"):

        resume_text = extract_text_from_docx(upload_path)

    else:

        return {
            "error": "Unsupported file format"
        }

    # AI Prompt
    prompt = f"""
    Analyze this resume carefully.

    Give:
    1. Resume Score out of 100
    2. Technical strengths
    3. Missing skills
    4. AI/ML job readiness
    5. Improvement suggestions

    Resume:
    {resume_text}
    """

    # Generate AI Response
    response = llm.invoke(prompt)

    return {
        "analysis": response.content
    }