from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from src.words.orm import SyncOrm

app = FastAPI(title="SecondDictionary")
templates = Jinja2Templates(directory="templates")


@app.get('/{item}/learned')
def select_learned(item: str, request: Request):
    iswords, h2 = (True, "Слово") if item == "words" else (False, "Фраза")
    return templates.TemplateResponse(
        request=request,
        name="learned.html",
        context={"h2": h2, "eng": SyncOrm.select_learned(iswords).model_dump()}
    )


@app.get('/{item}/random')
def get_random_word_or_phrase(item: str, request: Request):
    iswords, h2 = (True, "Слово") if item == "words" else (False, "Фраза")
    return templates.TemplateResponse(
        request=request,
        name="random_word_or_phrase.html",
        context={"eng_word": SyncOrm.get_random_eng_word(iswords).model_dump(), "h2": h2}
    )


@app.get('/{item}')
def get_words(request: Request, item: str):
    iswords, h2 = (True, "Слова") if item == "words" else (False, "Выражения")
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={"eng": SyncOrm.select_eng_words_or_phrases_orm(iswords).model_dump(), "h2": h2}
    )
