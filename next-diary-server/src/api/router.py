from fastapi import APIRouter
from src.api.routes import upload, diary

# 创建 API 路由器
api_router = APIRouter()

# 挂载路由
api_router.include_router(upload.router)
api_router.include_router(diary.router)