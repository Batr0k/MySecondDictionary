from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from src.words.orm import SyncOrm

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/phrases", tags=["phrases"])


@router.get('/testing')
def test(request: Request, verify_translate=Depends(SyncOrm.verify_translate_phrases)):
    if verify_translate[0]:
        status = "Правильно! Все переводы этого слова:"
    else:
        status = "Ошибка! Все переводы этого слова:"
    return templates.TemplateResponse(
        request=request,
        name="random_word_or_phrase_2.html",
        context={"eng": SyncOrm.get_random_eng_word(False).model_dump(), "status": status,
                 "router_prefix": router.prefix[1:],
                 "correct_translation": verify_translate[1]}
    )


@router.get('/')
def get_words(request: Request):
    return templates.TemplateResponse(
        request=request, name="learn.html",
        context={"eng": SyncOrm.select_eng_words_or_phrases_orm(False).model_dump()}
    )


@router.get('/random')
def get_random_word_or_phrase(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="random_word_or_phrase.html",
        context={"eng": SyncOrm.get_random_eng_word(False).model_dump(), "router_prefix": router.prefix[1:], }
    )


@router.get('/learned')
def select_learned(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="learned.html",
        context={"h2": "words", "eng": SyncOrm.select_learned(False).model_dump()}
    )


@router.get('/add')
def add_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="insert_eng_word_or_phrase.html",
        context={"router_prefix": router.prefix[1:]}
    )
@router.post('/')
def add_post(eng_word: str = Form(), ru_words: str = Form()):
    ru_words = list(map(str.strip, ru_words.lower().split(";")))
    return SyncOrm.insert_eng_word_and_translate_orm(False, eng_word, *ru_words)

