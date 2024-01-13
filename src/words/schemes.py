from pydantic import BaseModel


class EngWordsGetDTO(BaseModel):
    id: int
    eng: str
    ruwords: list["RuWordsGetDTO"]


class RuWordsGetDTO(BaseModel):
    id: int
    ru_word: str


class ListEngWordsGetDTO(BaseModel):
    List: list[EngWordsGetDTO]
