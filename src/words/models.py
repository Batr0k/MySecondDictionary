from sqlalchemy import Table, Column, Integer, MetaData, String, ForeignKey,text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, foreign, relationship
from datetime import datetime, UTC
from typing import Annotated
metadata = MetaData()
intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    pass


class EngWords(Base):
    __tablename__ = "eng_words"
    id: Mapped[intpk]
    eng_word: Mapped[str]
    date_Add: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    # ru_eng: Mapped[list["RuEng"]] = relationship(back_populates="eng_word")
class RuWords(Base):
    __tablename__ = "ru_words"
    id: Mapped[intpk]
    ru_word: Mapped[str]
    date_Add: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    # ru_eng: Mapped[list["RuEng"]] = relationship(back_populates="ru_word")
class RuEng(Base):
    __tablename__ = "ru_eng"
    id_ru: Mapped[int] = mapped_column(ForeignKey("ru_words.id"), primary_key=True)
    id_eng: Mapped[int] = mapped_column(ForeignKey("eng_words.id"), primary_key=True)
    # eng_word: Mapped["EngWords"] = relationship(back_populates="ru_eng")
    # ru_word: Mapped["RuWords"] = relationship(back_populates="ru_eng")
#
# eng_words = Table(
#     "eng_words",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("eng_word", String(30), nullable=False)
# )
# ru_words = Table(
#     "ru_words",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("ru_word", String, nullable=False)
# )
# ru_eng = Table(
#     "ru_eng",
#     metadata,
#     Column("id_ru", ForeignKey("ru_words.id")),
#     Column("id_eng", ForeignKey("eng_words.id"))
# )
