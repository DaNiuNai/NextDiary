import os
import secrets

from fastapi import APIRouter, UploadFile, File

from src.core.config import settings


router = APIRouter(prefix="/upload")


@router.post("/image", summary="上传图片")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片，保存到服务器并返回可访问的 URL。
    """
    image_dir_path = os.path.join(settings.RESOURCES_DIR_PATH, "images")
    # 生成一个安全随机的文件名
    file_ext = os.path.splitext(file.filename)[1]
    new_filename = f"{secrets.token_hex(16)}{file_ext}"
    file_path = os.path.join(image_dir_path, new_filename)

    # 写入文件到指定路径
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 返回图片的 URL
    return {"url": f"/resources/images/{new_filename}"}
