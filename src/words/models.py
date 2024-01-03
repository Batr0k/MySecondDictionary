from datetime import datetime, UTC
from typing import Annotated

from sqlalchemy import MetaData, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

metadata = MetaData()
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class EngWords(Base):
    __tablename__ = "eng_words"
    id: Mapped[intpk]
    eng: Mapped[str]
    date_add: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    ruwords: Mapped[list["RuWords"]] = relationship(back_populates="engwords", secondary="ru_eng_words")
    learned: Mapped["LearnedWords"] = relationship(back_populates="eng")


class EngPhrases(Base):
    __tablename__ = "eng_phrases"
    id: Mapped[intpk]
    eng: Mapped[str]
    date_add: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    ruwords: Mapped[list["RuWords"]] = relationship(back_populates="engphrases", secondary="ru_eng_phrases")
    learned: Mapped["LearnedPhrases"] = relationship(back_populates="eng")


class RuEngPhrases(Base):
    __tablename__ = "ru_eng_phrases"
    id_eng: Mapped[int] = mapped_column(ForeignKey("eng_phrases.id", ondelete="CASCADE"), primary_key=True)
    id_ru: Mapped[int] = mapped_column(ForeignKey("ru_words.id", ondelete="CASCADE"), primary_key=True)


class RuWords(Base):
    __tablename__ = "ru_words"
    id: Mapped[intpk]
    ru_word: Mapped[str]
    date_add: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    engwords: Mapped[list["EngWords"]] = relationship(back_populates="ruwords", secondary="ru_eng_words")
    engphrases: Mapped[list["EngPhrases"]] = relationship(back_populates="ruwords", secondary="ru_eng_phrases")


class RuEngWords(Base):
    __tablename__ = "ru_eng_words"
    id_ru: Mapped[int] = mapped_column(ForeignKey("ru_words.id", ondelete="CASCADE"), primary_key=True)
    id_eng: Mapped[int] = mapped_column(ForeignKey("eng_words.id", ondelete="CASCADE"), primary_key=True)

class LearnedPhrases(Base):
    __tablename__ = "learned_phrases"
    id: Mapped[int] = mapped_column(ForeignKey("eng_phrases.id", ondelete="CASCADE"), primary_key=True)
    eng: Mapped["EngPhrases"] = relationship(back_populates="learned")
class LearnedWords(Base):
    __tablename__ = "learned_words"
    id: Mapped[int] = mapped_column(ForeignKey("eng_words.id", ondelete="CASCADE"), primary_key=True)
    eng: Mapped["EngWords"] = relationship(back_populates="learned")

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
