from pydantic import BaseModel


class EngWordsGetDTO(BaseModel):
    id: int
    eng_word: str
    ruwords: list["RuWordsGetDTO"]


class RuWordsGetDTO(BaseModel):
    id: int
    ru_word: str


class ListEngWordsGetDTO(BaseModel):
    List: list[EngWordsGetDTO]


class EngWordRandomGetDTO(BaseModel):
    id: int
    eng_word: str
