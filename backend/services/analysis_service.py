import re

from repositories.user_repository import UserRepository
from repositories.analysis_repository import AnalysisRepository

from services.ai_service import generate_response


class AnalysisService:

    def __init__(
        self,
        user_repo: UserRepository,
        analysis_repo: AnalysisRepository
    ):
        self.user_repo = user_repo
        self.analysis_repo = analysis_repo

    def analyze_resume(
        self,
        user_email: str,
        filename: str,
        resume_text: str
    ):

        user = self.user_repo.get_by_email(
            user_email
        )

        if not user:
            raise Exception(
                "User not found"
            )

        prompt = f"""
        Analyze this resume carefully.

        Give:

        1. ATS Score (0-100)
        2. Resume Summary
        3. Technical Skills Found
        4. Missing Skills
        5. AI/ML Job Readiness
        6. Strengths
        7. Weaknesses
        8. Suggestions for Improvement
        9. Hiring Recommendation

        Resume:
        {resume_text}
        """

        result = generate_response(
            prompt
        )

        ats_score = self.extract_ats_score(
            result
        )

        analysis = (
            self.analysis_repo.create(
                user_id=user.id,
                filename=filename,
                ats_score=ats_score,
                analysis=result
            )
        )

        return {
            "analysis": analysis,
            "ats_score": ats_score,
            "result": result
        }

    def extract_ats_score(
        self,
        text: str
    ) -> int:

        patterns = [
            r'ATS\s*Score\s*\(0-100\)\s*:\s*(\d{1,3})',
            r'ATS\s*Score\s*:\s*(\d{1,3})',
            r'\*\*ATS\s*Score.*?(\d{2,3})'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return int(
                    match.group(1)
                )

        return 0