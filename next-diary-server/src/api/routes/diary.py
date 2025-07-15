from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func

from src.core.database import get_session
from src.models.response.diary import DiaryReadWithComments
from src.models.request.diary import DiaryCreate
from src.models.request.comment import CommentCreate
from src.models.database.mapping import Diary, Comment
from src.models.response.comment import CommentRead


router = APIRouter(prefix="/diary")


@router.post(
    "/exchange", response_model=DiaryReadWithComments, summary="提交日记并交换"
)
def exchange_diary(
    *, session: Session = Depends(get_session), diary_create: DiaryCreate
):
    """
    1. 创建一篇新日记。
    2. 从数据库中随机选择一篇别人的日记返回。
    """
    # 1. 创建新日记
    db_diary = Diary.model_validate(diary_create)
    session.add(db_diary)
    session.commit()
    session.refresh(db_diary)

    # 2. 随机获取一篇不是刚刚提交的日记
    # 首先计算总数
    total_diaries = session.exec(select(func.count(Diary.id))).one()

    if total_diaries <= 1:
        raise HTTPException(status_code=404, detail="日记池中还没有其他日记可供交换")

    # 随机选择一篇
    random_diary = session.exec(
        select(Diary).where(Diary.id != db_diary.id).order_by(func.random()).limit(1)
    ).first()

    return random_diary


@router.post("/add-comments", response_model=CommentRead, summary="添加评论")
def create_comment_for_diary(
    *, session: Session = Depends(get_session), comment: CommentCreate
):
    """
    为指定的日记添加一条新评论。
    """
    diary = session.get(Diary, comment.diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    db_comment = Comment(
        author=comment.author, content=comment.content, diary_id=diary.id
    )
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment
