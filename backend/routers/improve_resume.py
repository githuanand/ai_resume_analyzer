from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from database.db import get_db

from repositories.user_repository import UserRepository
from repositories.analysis_repository import AnalysisRepository
from repositories.improvement_repository import ImprovementRepository

from services.jwt_service import get_current_user
from services.resume_improvement_service import improve_resume


router = APIRouter()


class ImproveResumeRequest(BaseModel):
    analysis_id: int


@router.post("/improve-resume")
def improve_resume_endpoint(
    request: ImproveResumeRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)
    analysis_repo = AnalysisRepository(db)
    improvement_repo = ImprovementRepository(db)

    user = user_repo.get_by_email(
        current_user
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    analysis = analysis_repo.get_user_analysis(
        request.analysis_id,
        user.id
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    result = improve_resume(
        analysis.analysis
    )

    improvement = improvement_repo.create(
        user_id=user.id,
        analysis_id=analysis.id,
        improved_resume=result
    )

    return {
        "improvement_id": improvement.id,
        "analysis_id": analysis.id,
        "filename": analysis.filename,
        "improved_resume": result
    }


@router.get("/my-improvements")
def get_my_improvements(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)
    improvement_repo = ImprovementRepository(db)

    user = user_repo.get_by_email(
        current_user
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    improvements = (
        improvement_repo.get_user_improvements(
            user.id
        )
    )

    return improvements


@router.get("/improvement/{improvement_id}")
def get_improvement(
    improvement_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)
    improvement_repo = ImprovementRepository(db)

    user = user_repo.get_by_email(
        current_user
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    improvement = (
        improvement_repo.get_by_id(
            improvement_id,
            user.id
        )
    )

    if not improvement:
        raise HTTPException(
            status_code=404,
            detail="Improvement not found"
        )

    return improvement