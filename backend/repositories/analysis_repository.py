from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Analysis


class AnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        analysis_id: int
    ):

        return (
            self.db.query(Analysis)
            .filter(
                Analysis.id == analysis_id
            )
            .first()
        )

    def get_user_analysis(
        self,
        analysis_id: int,
        user_id: int
    ):

        return (
            self.db.query(Analysis)
            .filter(
                Analysis.id == analysis_id,
                Analysis.user_id == user_id
            )
            .first()
        )

    def create(
        self,
        user_id: int,
        filename: str,
        ats_score: int,
        analysis: str
    ):

        record = Analysis(
            user_id=user_id,
            filename=filename,
            ats_score=ats_score,
            analysis=analysis
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record

    def get_user_analyses(
        self,
        user_id: int
    ):

        return (
            self.db.query(Analysis)
            .filter(
                Analysis.user_id == user_id
            )
            .order_by(
                Analysis.created_at.desc()
            )
            .all()
        )

    def count_user_analyses(
        self,
        user_id: int
    ):

        return (
            self.db.query(Analysis)
            .filter(
                Analysis.user_id == user_id
            )
            .count()
        )

    def get_average_score(
        self,
        user_id: int
    ):

        return (
            self.db.query(
                func.avg(
                    Analysis.ats_score
                )
            )
            .filter(
                Analysis.user_id == user_id
            )
            .scalar()
        )

    def get_best_score(
        self,
        user_id: int
    ):

        return (
            self.db.query(
                func.max(
                    Analysis.ats_score
                )
            )
            .filter(
                Analysis.user_id == user_id
            )
            .scalar()
        )

    def get_latest_analysis(
        self,
        user_id: int
    ):

        return (
            self.db.query(Analysis)
            .filter(
                Analysis.user_id == user_id
            )
            .order_by(
                Analysis.created_at.desc()
            )
            .first()
        )