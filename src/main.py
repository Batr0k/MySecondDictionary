from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.words.orm import SyncOrm
from src.words.router_phrases import router as phrases_router
from src.words.router_words import router as words_router

app = FastAPI(title="SecondDictionary")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(words_router)
app.include_router(phrases_router)


@app.get('/')
def start(request: Request):
    return templates.TemplateResponse(
        request=request, name="start.html",
    )
