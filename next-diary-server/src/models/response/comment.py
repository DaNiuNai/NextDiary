from datetime import datetime
from pydantic import BaseModel

class CommentRead(BaseModel):
    id: int
    author: str
    content: str
    create_time: datetime
