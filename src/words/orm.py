from random import choice

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload

from src.words.database import engine, session_factory
from src.words.models import EngWords, Base, RuWords, LearnedWords, RuEngWords, EngPhrases, RuEngPhrases, LearnedPhrases
from src.words.schemes import EngWordsGetDTO, ListEngWordsGetDTO


class SyncOrm:
    @staticmethod
    def create_table_orm():
        Base.metadata.create_all(engine)

    @staticmethod
    def insert_eng_word_and_translate_orm(word: str, istablewords: bool = True, *args):
        with session_factory() as session:
            table = EngWords if istablewords else EngPhrases
            new_eng = table(eng=word)
            new_ru_words = [RuWords(ru_word=i) for i in args]
            new_eng.ruwords = new_ru_words
            session.add(new_eng)
            session.commit()

    @staticmethod
    def delete_word(id: int, iswords: bool = True):
        with session_factory() as session:
            table, subtable = (EngWords, RuEngWords) if iswords else (EngPhrases, RuEngPhrases)
            subquery = select(subtable.id_ru).where(subtable.id_eng == id)
            stmt = delete(RuWords).where(RuWords.id.in_(subquery))
            session.execute(stmt)
            stmt = delete(EngWords).where(EngWords.id == id)
            session.execute(stmt)
            session.commit()

    @staticmethod
    def select_eng_words_or_phrases_orm(iswords: bool):
        table, learned = (EngWords, LearnedWords) if iswords else (EngPhrases, LearnedPhrases)
        with session_factory() as session:
            query = select(table).join(learned, learned.id == table.id,
                                       isouter=True).where(learned.id == None).options(
                selectinload(table.ruwords)).options(
                joinedload(table.learned))
            res = session.execute(query).scalars().all()
            res_dto = [EngWordsGetDTO.model_validate(row, from_attributes=True) for row in res]
            res_dto = ListEngWordsGetDTO(List=res_dto)
            return res_dto

    @staticmethod
    def select_learned(iswords: bool):
        table, learned = (EngWords, LearnedWords) if iswords else (EngPhrases, LearnedPhrases)
        with session_factory() as session:
            query = select(table).join(learned, learned.id == table.id)
            res = session.execute(query).scalars().all()
            res_dto = [EngWordsGetDTO.model_validate(row, from_attributes=True) for row in res]
            res_dto = ListEngWordsGetDTO(List=res_dto)
            return res_dto

    @staticmethod
    def get_random_eng_word(iswords: bool):
        table, learned = (EngWords, LearnedWords) if iswords else (EngPhrases, LearnedPhrases)
        with session_factory() as session:
            query = select(table).join(learned, learned.id == table.id,
                                       isouter=True).where(learned.id == None).options(
                selectinload(table.ruwords)).options(
                joinedload(table.learned))
            res = choice(session.execute(query).scalars().all())
            res_dto = EngWordsGetDTO.model_validate(res, from_attributes=True)
            return res_dto

    @staticmethod
    def insert_to_learned(id: int, iswords: bool):
        with session_factory() as session:
            learned = LearnedWords if iswords else LearnedPhrases
            l = learned(id=id)
            session.add(l)
            session.commit()

    @staticmethod
    def delete_table_orm():
        Base.metadata.drop_all(engine)
