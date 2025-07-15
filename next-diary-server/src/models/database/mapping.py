from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: str  # 作者
    content: str  # 评论内容
    # 创建时间
    create_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
    )
    diary_id: int = Field(foreign_key="diary.id")  # 关联到的日记

    diary: "Diary" = Relationship(back_populates="comments")  # 关联的日记


class Diary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: str  # 作者
    content: str  # 日记内容
    # 创建时间
    create_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
    )

    comments: list["Comment"] | None = Relationship(
        back_populates="diary"
    )  # 关联的评论
