import json
import re

from services.ai_service import generate_response


def match_resume_job(
    resume_text: str,
    job_description: str
):

    prompt = f"""
    Compare the resume and job description.

    Return ONLY JSON.

    Example:

    {{
        "match_score": 85,
        "strong_skills": ["Python"],
        "missing_skills": ["AWS"],
        "recommendations": ["Learn AWS"]
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    response = generate_response(prompt)

    try:
        return json.loads(response)

    except Exception:

        match = re.search(
            r'\{.*\}',
            response,
            re.DOTALL
        )

        if match:
            return json.loads(match.group())

        return {
            "error": "Invalid AI response",
            "raw_response": response
        }