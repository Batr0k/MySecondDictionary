from random import choice

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload

from src.words.database import engine, session_factory
from src.words.models import EngWords, Base, RuWords, LearnedWords, RuEngWords, EngPhrases, RuEngPhrases
from src.words.schemes import EngWordsGetDTO, EngWordRandomGetDTO, ListEngWordsGetDTO


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
    def delete_word(ID: int, istablewords: bool = True):
        with session_factory() as session:
            table, subtable = (EngWords, RuEngWords) if istablewords else (EngPhrases, RuEngPhrases)
            subquery = select(subtable.id_ru).where(subtable.id_eng == ID)
            stmt = delete(RuWords).where(RuWords.id.in_(subquery))
            session.execute(stmt)
            stmt = delete(EngWords).where(EngWords.id == ID)
            session.commit()

    @staticmethod
    def select_eng_words_orm():
        with session_factory() as session:
            query = select(EngWords).select_from(EngWords).join(LearnedWords, LearnedWords.id == EngWords.id,
                                                                isouter=True).where(LearnedWords.id == None).options(
                selectinload(EngWords.ruwords)).options(
                joinedload(EngWords.learned_word))
            res = session.execute(query).scalars().all()
            res_dto = [EngWordsGetDTO.model_validate(row, from_attributes=True) for row in res]
            res_dto = ListEngWordsGetDTO(List=res_dto)
            return res_dto

    @staticmethod
    def get_random_eng_word():
        with session_factory() as session:
            query = select(EngWords).select_from(EngWords).join(LearnedWords, LearnedWords.id == EngWords.id,
                                                                isouter=True).where(LearnedWords.id == None).options(
                selectinload(EngWords.ruwords)).options(
                joinedload(EngWords.learned_word))
            res = choice(session.execute(query).scalars().all())
            res_dto = EngWordRandomGetDTO.model_validate(res, from_attributes=True)
            return res_dto

    @staticmethod
    def insert_to_learned(id: int):
        with session_factory() as session:
            lw = LearnedWords(id=id)
            session.add(lw)
            session.commit()

    @staticmethod
    def delete_table_orm():
        Base.metadata.drop_all(engine)
