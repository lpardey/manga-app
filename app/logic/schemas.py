from pydantic import BaseModel


class Image(BaseModel):
    number: int | None = None
    source: str


class Chapter(BaseModel):
    number: int | None = None
    name: str
    images: list[Image]
