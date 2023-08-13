from models.progress_indicator import ProgressIndicator
from fastapi import APIRouter
from repositories.progress_indicator_repository import ProgressIndicatorRepository

router = APIRouter()

get_progress_indicator_repository = ProgressIndicatorRepository()

@router.get("/")
def get_progress_indicator():
    progress_indicator = get_progress_indicator_repository.get_current_indicator()
    return ProgressIndicator(**progress_indicator)