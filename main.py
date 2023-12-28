from fastapi import FastAPI

from src.words.router import router as words_page

app = FastAPI(title="SecondDictionary")
app.include_router(words_page)
