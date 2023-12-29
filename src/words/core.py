from sqlalchemy import create_engine, insert, delete, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from src.words.models import metadata, EngWords, Base

async_engine = create_async_engine(
    url=settings.async_refer_to_db(),
    # echo=True,
    # pool_size=5,
    # max_overflow=10
)
engine = create_engine(
    url=settings.sync_refer_to_db(),
    echo=True
)
session_factory = sessionmaker(engine)


# def insert_eng_word_core():
#     with engine.connect() as conn:
#         stmt = insert(eng_words).values({"eng_word": "home"})
#         conn.execute(stmt)
#         conn.commit()


def create_table_core():
    metadata.create_all(engine)


def create_table_orm():
    Base.metadata.create_all(engine)


def insert_eng_words_orm():
    with session_factory() as session:
        for i in ("prevent", "cat", "home", "commit"):
            session.execute(insert(EngWords).values({"eng_word": i}))
        session.commit()

def delete_eng_words_orm():
    with session_factory() as session:
        session.execute(delete(EngWords))
        session.commit()
def select_eng_words_orm():
    with session_factory() as session:
        query = select(EngWords)
        session.execute(query)
        session.commit()
def delete_table_core():
    metadata.drop_all(engine)


def delete_table_orm():
    Base.metadata.drop_all(engine)
