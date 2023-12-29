from fastapi import FastAPI

from src.words.router import router as words_page
from src.words.core import insert_eng_words_orm, create_table_orm, delete_table_orm, delete_eng_words_orm, select_eng_words_orm
app = FastAPI(title="SecondDictionary")
app.include_router(words_page)
# delete_table_orm()
# insert_eng_words_orm()
select_eng_words_orm()
# create_table_orm()
# delete_eng_words_orm()