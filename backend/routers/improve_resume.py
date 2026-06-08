from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from services.jwt_service import get_current_user

from services.improvement_service import (
    ImprovementService
)

from dependencies.services import (
    get_improvement_service
)


router = APIRouter()


class ImproveResumeRequest(BaseModel):
    analysis_id: int


@router.post("/improve-resume")
def improve_resume_endpoint(

    request: ImproveResumeRequest,

    current_user: str = Depends(
        get_current_user
    ),

    improvement_service: ImprovementService = Depends(
        get_improvement_service
    )

):

    try:

        result = (
            improvement_service.improve_resume(
                user_email=current_user,
                analysis_id=request.analysis_id
            )
        )

        improvement = result["improvement"]

        analysis = result["analysis"]

        return {
            "improvement_id": improvement.id,
            "analysis_id": analysis.id,
            "filename": analysis.filename,
            "improved_resume": result["result"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/my-improvements")
def get_my_improvements(

    current_user: str = Depends(
        get_current_user
    ),

    improvement_service: ImprovementService = Depends(
        get_improvement_service
    )

):

    try:

        return (
            improvement_service
            .get_user_improvements(
                current_user
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/improvement/{improvement_id}")
def get_improvement(

    improvement_id: int,

    current_user: str = Depends(
        get_current_user
    ),

    improvement_service: ImprovementService = Depends(
        get_improvement_service
    )

):

    try:

        return (
            improvement_service
            .get_improvement(
                user_email=current_user,
                improvement_id=improvement_id
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )