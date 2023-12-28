from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/words",
                   tags=["words"])
templates = Jinja2Templates(directory="templates")


@router.get('/')
def get_words(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
