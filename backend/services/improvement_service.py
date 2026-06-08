from repositories.user_repository import UserRepository
from repositories.analysis_repository import AnalysisRepository
from repositories.improvement_repository import ImprovementRepository

from services.resume_improvement_service import (
    improve_resume
)


class ImprovementService:

    def __init__(
        self,
        user_repo: UserRepository,
        analysis_repo: AnalysisRepository,
        improvement_repo: ImprovementRepository
    ):
        self.user_repo = user_repo
        self.analysis_repo = analysis_repo
        self.improvement_repo = improvement_repo

    def improve_resume(
        self,
        user_email: str,
        analysis_id: int
    ):

        user = self.user_repo.get_by_email(
            user_email
        )

        if not user:
            raise Exception(
                "User not found"
            )

        analysis = (
            self.analysis_repo.get_user_analysis(
                analysis_id,
                user.id
            )
        )

        if not analysis:
            raise Exception(
                "Analysis not found"
            )

        result = improve_resume(
            analysis.analysis
        )

        improvement = (
            self.improvement_repo.create(
                user_id=user.id,
                analysis_id=analysis.id,
                improved_resume=result
            )
        )

        return {
            "improvement": improvement,
            "analysis": analysis,
            "result": result
        }

    def get_user_improvements(
        self,
        user_email: str
    ):

        user = self.user_repo.get_by_email(
            user_email
        )

        if not user:
            raise Exception(
                "User not found"
            )

        return (
            self.improvement_repo
            .get_user_improvements(
                user.id
            )
        )

    def get_improvement(
        self,
        user_email: str,
        improvement_id: int
    ):

        user = self.user_repo.get_by_email(
            user_email
        )

        if not user:
            raise Exception(
                "User not found"
            )

        improvement = (
            self.improvement_repo.get_by_id(
                improvement_id,
                user.id
            )
        )

        if not improvement:
            raise Exception(
                "Improvement not found"
            )

        return improvement