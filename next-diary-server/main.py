# backend/main.py
import os
import secrets
from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func

from database import get_session, create_db_and_tables
from models import (
    Diary,
    DiaryCreate,
    DiaryRead,
    DiaryReadWithComments,
    Comment,
    CommentCreate,
    CommentRead,
)

# 创建静态文件目录
os.makedirs("static/images", exist_ok=True)

app = FastAPI(title="日记互换 API")

# 配置 CORS 中间件，允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许你的 Vue 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录，用于访问上传的图片
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/upload-image/", summary="上传图片")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片，保存到服务器并返回可访问的 URL。
    """
    # 生成一个安全随机的文件名
    file_ext = os.path.splitext(file.filename)[1]
    new_filename = f"{secrets.token_hex(16)}{file_ext}"
    file_path = f"static/images/{new_filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 返回图片的 URL
    return {"url": f"/static/images/{new_filename}"}


@app.post("/exchange/", response_model=DiaryReadWithComments, summary="提交日记并交换")
def exchange_diary(
    *, session: Session = Depends(get_session), diary_create: DiaryCreate
):
    """
    1. 创建一篇新日记。
    2. 从数据库中随机选择一篇别人的日记返回。
    """
    # 1. 创建新日记
    db_diary = Diary.from_orm(diary_create)
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

    if not random_diary:
        # 理论上，在 total_diaries > 1 的情况下不会发生
        raise HTTPException(status_code=404, detail="找不到可交换的日记")

    return random_diary


@app.post(
    "/diaries/{diary_id}/comments/", response_model=CommentRead, summary="添加评论"
)
def create_comment_for_diary(
    diary_id: int, *, session: Session = Depends(get_session), comment: CommentCreate
):
    """
    为指定的日记添加一条新评论。
    """
    diary = session.get(Diary, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")

    db_comment = Comment.from_orm(comment, update={"diary_id": diary_id})
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
