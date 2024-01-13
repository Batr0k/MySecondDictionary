from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from src.words.orm import SyncOrm

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/words", tags=["words"])

@router.get('/testing')
def test(request: Request, verify_translate=Depends(SyncOrm.verify_translate_words)):
    if verify_translate[0]:
        status = "Правильно! Все переводы этого слова:"
    else:
        status = "Ошибка! Все переводы этого слова:"
    return templates.TemplateResponse(
        request=request,
        name="random_word_or_phrase_2.html",
        context={"eng": SyncOrm.get_random_eng_word(True).model_dump(), "status": status, "router_prefix": router.prefix[1:],
                 "correct_translation": verify_translate[1]}
    )


@router.get('/')
def get_words(request: Request):
    return templates.TemplateResponse(
        request=request, name="learn.html",
        context={"eng": SyncOrm.select_eng_words_or_phrases_orm(True).model_dump(), "router_prefix": router.prefix[1:]}
    )


@router.get('/random')
def get_random_word_or_phrase(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="random_word_or_phrase.html",
        context={"eng": SyncOrm.get_random_eng_word(True).model_dump(), "router_prefix": router.prefix[1:],}
    )


@router.get('/learned')
def select_learned(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="learned.html",
        context={ "router_prefix": router.prefix[1:], "eng": SyncOrm.select_learned(True).model_dump()}
    )
@router.get('/add')
def add(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="insert_eng_word_or_phrase.html",
        context= { "router_prefix": router.prefix[1:]}
    )
@router.post('/')
def add_post(request: Request, eng_word: str = Form(), ru_words: str = Form()):
    ru_words = list(map(str.strip, ru_words.lower().split(";")))
    return templates.TemplateResponse(
        request=request,
        name="insert_eng_word_or_phrase_2.html",
        context={"router_prefix": router.prefix[1:],
                 "status": SyncOrm.insert_eng_word_and_translate_orm(True, eng_word, *ru_words)}
    )
@router.get('/delete/{id}')
def delete_word(id: int):
    SyncOrm.delete_word(id, True)
    return RedirectResponse("/words")


@router.get('/learned/{id}')
def insert_to_learned(id: int):
    SyncOrm.insert_to_learned(id, True)
    return RedirectResponse("/words")
@router.get('/deletelearned/{id}')
def delete_from_learned(id:int):
    SyncOrm.delete_from_learned(id,True)
    return RedirectResponse("/words/learned")