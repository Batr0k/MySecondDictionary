from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.words.orm import SyncOrm

router = APIRouter(prefix="/words",
                   tags=["words"])

templates = Jinja2Templates(directory="templates")


@router.get('/')
def get_words(request: Request):

    return templates.TemplateResponse(
        request=request, name="index.html", context={"eng_words": SyncOrm.select_eng_words_orm().model_dump()}
    )
