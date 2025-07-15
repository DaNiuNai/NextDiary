import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.core.config import settings
from src.core.database import create_db_and_tables
from src.api.router import api_router


os.makedirs(os.path.join(settings.RESOURCES_DIR_PATH, "images"), exist_ok=True)

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

# 挂载 API 路由
app.include_router(api_router)

# 挂载静态文件目录，用于访问上传的图片
app.mount(
    f"/resources", StaticFiles(directory=settings.RESOURCES_DIR_PATH), name="resources"
)

# 创建数据库和表
create_db_and_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
