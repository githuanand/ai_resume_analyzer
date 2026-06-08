from fastapi import Depends

from repositories.user_repository import UserRepository
from repositories.analysis_repository import AnalysisRepository
from repositories.improvement_repository import ImprovementRepository

from dependencies.repositories import (
    get_user_repository,
    get_analysis_repository,
    get_improvement_repository
)

from services.user_service import UserService
from services.analysis_service import AnalysisService
from services.improvement_service import ImprovementService
from services.dashboard_service import DashboardService


def get_user_service(

    user_repo: UserRepository = Depends(
        get_user_repository
    )

):

    return UserService(
        user_repo=user_repo
    )


def get_analysis_service(

    user_repo: UserRepository = Depends(
        get_user_repository
    ),

    analysis_repo: AnalysisRepository = Depends(
        get_analysis_repository
    )

):

    return AnalysisService(
        user_repo=user_repo,
        analysis_repo=analysis_repo
    )


def get_improvement_service(

    user_repo: UserRepository = Depends(
        get_user_repository
    ),

    analysis_repo: AnalysisRepository = Depends(
        get_analysis_repository
    ),

    improvement_repo: ImprovementRepository = Depends(
        get_improvement_repository
    )

):

    return ImprovementService(
        user_repo=user_repo,
        analysis_repo=analysis_repo,
        improvement_repo=improvement_repo
    )


def get_dashboard_service(

    user_repo: UserRepository = Depends(
        get_user_repository
    ),

    analysis_repo: AnalysisRepository = Depends(
        get_analysis_repository
    )

):

    return DashboardService(
        user_repo=user_repo,
        analysis_repo=analysis_repo
    )