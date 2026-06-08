import os

from uuid import uuid4

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from database.db import get_db

from repositories.user_repository import UserRepository
from repositories.analysis_repository import AnalysisRepository

from services.resume_service import ResumeService
from services.analysis_service import AnalysisService
from services.jwt_service import get_current_user

from utils.pdf_generator import generate_pdf_report


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = os.path.join(
        "uploads",
        f"{uuid4()}_{file.filename}"
    )

    with open(
        file_path,
        "wb"
    ) as f:
        f.write(
            await file.read()
        )

    resume_service = ResumeService()

    resume_text = (
        resume_service.extract_text(
            file_path
        )
    )

    user_repo = UserRepository(db)

    analysis_repo = AnalysisRepository(db)

    analysis_service = AnalysisService(
        user_repo=user_repo,
        analysis_repo=analysis_repo
    )

    result = (
        analysis_service.analyze_resume(
            user_email=current_user,
            filename=file.filename,
            resume_text=resume_text
        )
    )

    analysis = result["analysis"]

    return {
        "status": "success",
        "user": current_user,
        "analysis_id": analysis.id,
        "filename": file.filename,
        "ats_score": result["ats_score"],
        "analysis": result["result"]
    }


@router.get("/my-analyses")
def get_my_analyses(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)
    analysis_repo = AnalysisRepository(db)

    user = user_repo.get_by_email(
        current_user
    )

    if not user:
        return []

    analyses = analysis_repo.get_user_analyses(
        user.id
    )

    return analyses


@router.get("/dashboard")
def dashboard(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)
    analysis_repo = AnalysisRepository(db)

    user = user_repo.get_by_email(
        current_user
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    total_analyses = (
        analysis_repo.count_user_analyses(
            user.id
        )
    )

    avg_score = (
        analysis_repo.get_average_score(
            user.id
        )
    )

    best_score = (
        analysis_repo.get_best_score(
            user.id
        )
    )

    latest_analysis = (
        analysis_repo.get_latest_analysis(
            user.id
        )
    )

    return {
        "user": user.email,
        "total_analyses": total_analyses,
        "average_ats_score": (
            round(float(avg_score), 2)
            if avg_score
            else 0
        ),
        "best_ats_score": (
            int(best_score)
            if best_score
            else 0
        ),
        "latest_analysis_id": (
            latest_analysis.id
            if latest_analysis
            else None
        ),
        "latest_analysis_date": (
            latest_analysis.created_at
            if latest_analysis
            else None
        )
    }


@router.get("/report/{analysis_id}")
def download_report(
    analysis_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_repo = UserRepository(db)
    analysis_repo = AnalysisRepository(db)

    user = user_repo.get_by_email(
        current_user
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    analysis = analysis_repo.get_user_analysis(
        analysis_id,
        user.id
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    os.makedirs(
        "reports",
        exist_ok=True
    )

    pdf_path = generate_pdf_report(
        f"analysis_{analysis.id}",
        analysis.analysis
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"analysis_{analysis.id}.pdf"
    )