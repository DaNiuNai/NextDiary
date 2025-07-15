from datetime import datetime
from pydantic import BaseModel
from typing import List
from src.models.response.comment import CommentRead

class DiaryReadWithComments(BaseModel):
    id: int
    author: str
    content: str
    create_time: datetime
    comments: List["CommentRead"] = list()