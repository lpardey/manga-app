from pydantic import BaseModel

class Image(BaseModel):
    number: int
    source: str


class Chapter(BaseModel):
    number: int
    name: str
    images: list[Image]
