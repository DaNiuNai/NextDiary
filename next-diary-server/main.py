import os
import secrets

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select, func

from src.core.config import settings
from src.core.database import create_db_and_tables, get_session
from src.models.response.diary import DiaryReadWithComments
from src.models.response.comment import CommentRead

from src.models.request.diary import DiaryCreate
from src.models.request.comment import CommentCreate

from src.models.database.mapping import Diary, Comment


image_dir_path = os.path.join(settings.RESOURCES_DIR_PATH, "images")
os.makedirs(image_dir_path, exist_ok=True)

app = FastAPI(title="Next Diary API")


# 配置 CORS 中间件，允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的来源列表，"*" 表示允许所有来源
    allow_credentials=True,  # 允许携带认证信息（cookies, authorization headers等）
    allow_methods=[
        "*"
    ],  # 允许的 HTTP 方法列表，"*" 表示允许所有方法 (GET, POST, OPTIONS等)
    allow_headers=["*"],  # 允许的请求头部列表，"*" 表示允许所有头部
)

# 挂载静态文件目录，用于访问上传的图片
app.mount(f"/resources", StaticFiles(directory=settings.RESOURCES_DIR_PATH), name="resources")

# 创建数据库和表
create_db_and_tables()


@app.post("/upload-image/", summary="上传图片")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片，保存到服务器并返回可访问的 URL。
    """
    # 生成一个安全随机的文件名
    file_ext = os.path.splitext(file.filename)[1]
    new_filename = f"{secrets.token_hex(16)}{file_ext}"
    file_path = os.path.join(image_dir_path, new_filename)

    # 写入文件到指定路径
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 返回图片的 URL
    return {"url": f"/resources/images/{new_filename}"}


@app.post("/exchange/", response_model=DiaryReadWithComments, summary="提交日记并交换")
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

    db_comment = Comment.model_validate(comment, update={"diary_id": diary_id})
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
