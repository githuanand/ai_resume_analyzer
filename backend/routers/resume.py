
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
from services.dashboard_service import DashboardService
from services.jwt_service import get_current_user

from dependencies.services import (
    get_analysis_service,
    get_dashboard_service
)

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

    current_user: str = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    ),

    analysis_service: AnalysisService = Depends(
        get_analysis_service
    )
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
    current_user: str = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    user_repo = UserRepository(db)

    analysis_repo = AnalysisRepository(db)

    user = user_repo.get_by_email(
        current_user
    )

    if not user:
        return []

    return (
        analysis_repo.get_user_analyses(
            user.id
        )
    )


@router.get("/dashboard")
def dashboard(

    current_user: str = Depends(
        get_current_user
    ),

    dashboard_service: DashboardService = Depends(
        get_dashboard_service
    )

):

    try:

        return (
            dashboard_service
            .get_dashboard_data(
                current_user
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/report/{analysis_id}")
def download_report(
    analysis_id: int,

    current_user: str = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
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

    analysis = (
        analysis_repo.get_user_analysis(
            analysis_id,
            user.id
        )
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

