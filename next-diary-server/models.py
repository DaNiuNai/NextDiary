# backend/models.py
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# ==================================
# 评论模型
# ==================================
class CommentBase(SQLModel):
    author: str
    content: str

class Comment(CommentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    diary_id: int = Field(foreign_key="diary.id")
    diary: "Diary" = Relationship(back_populates="comments")

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    created_at: datetime

# ==================================
# 日记模型
# ==================================
class DiaryBase(SQLModel):
    author: str
    content: str  # 存储富文本 HTML

class Diary(DiaryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    comments: List["Comment"] = Relationship(back_populates="diary")

class DiaryCreate(DiaryBase):
    pass

class DiaryRead(DiaryBase):
    id: int
    created_at: datetime

class DiaryReadWithComments(DiaryRead):
    comments: List[CommentRead] = []

