from pydantic import BaseModel


class CommentCreate(BaseModel):
    author: str
    content: str
    diary_id: int

