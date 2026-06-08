from fastapi import Depends
from sqlalchemy.orm import Session

from database.db import get_db

from repositories.user_repository import UserRepository
from repositories.analysis_repository import AnalysisRepository
from repositories.improvement_repository import ImprovementRepository


def get_user_repository(
    db: Session = Depends(get_db)
):
    return UserRepository(db)


def get_analysis_repository(
    db: Session = Depends(get_db)
):
    return AnalysisRepository(db)


def get_improvement_repository(
    db: Session = Depends(get_db)
):
    return ImprovementRepository(db)