import json

from src.words.orm import SyncOrm
def import_words_and_phrases(fileName: str):
    iswords = True if "words" in fileName[fileName.rfind("\\"):] else False
    with open(fileName, encoding="utf-8") as file:
        words = json.load(file)
        for word in words:
            SyncOrm.insert_eng_word_and_translate_orm(iswords, word, *words[word])
import_words_and_phrases(r"D:\ProgramsAndApps\dist\main\jsonfiles\mydictionaryphrases.json")