from sqlalchemy.orm import Session

from database.models import ResumeImprovement


class ImprovementRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        analysis_id: int,
        improved_resume: str
    ):

        improvement = ResumeImprovement(
            user_id=user_id,
            analysis_id=analysis_id,
            improved_resume=improved_resume
        )

        self.db.add(improvement)
        self.db.commit()
        self.db.refresh(improvement)

        return improvement

    def get_by_id(
        self,
        improvement_id: int,
        user_id: int
    ):

        return (
            self.db.query(
                ResumeImprovement
            )
            .filter(
                ResumeImprovement.id == improvement_id,
                ResumeImprovement.user_id == user_id
            )
            .first()
        )

    def get_user_improvements(
        self,
        user_id: int
    ):

        return (
            self.db.query(
                ResumeImprovement
            )
            .filter(
                ResumeImprovement.user_id == user_id
            )
            .order_by(
                ResumeImprovement.created_at.desc()
            )
            .all()
        )