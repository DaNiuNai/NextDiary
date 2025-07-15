from pydantic import BaseModel


class DiaryCreate(BaseModel):
    author: str
    content: str
