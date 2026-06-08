from services.ai_service import generate_response


def improve_resume(
    resume_analysis: str
):

    prompt = f"""
    You are an expert Resume Writer.

    IMPORTANT RULES:

    1. Do NOT invent information.
    2. Do NOT create fake phone numbers.
    3. Do NOT create fake email addresses.
    4. Do NOT create fake certifications.
    5. Do NOT create fake projects.
    6. Do NOT create fake skills.
    7. Use ONLY information already present in the resume analysis.
    8. If information is missing, write:
       [ADD DETAILS]

    Based on this resume analysis:

    {resume_analysis}

    Generate:

    1. Improved Professional Summary
    2. Improved Skills Section
    3. Improved Project Descriptions
    4. Improved Resume Version

    Return clearly formatted text.
    """

    return generate_response(prompt)