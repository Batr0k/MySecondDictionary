from fastapi import FastAPI

from src.words.router import router as words_page

from src.words.orm import SyncOrm

app = FastAPI(title="SecondDictionary")
# SyncOrm.insert_eng_word_and_translate_orm("because of", False, "из-за")
# SyncOrm.delete_word(1, False)
# SyncOrm.delete_table_orm()
# SyncOrm.create_table_orm()
