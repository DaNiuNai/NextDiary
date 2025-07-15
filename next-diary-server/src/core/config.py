from pydantic_settings import BaseSettings
import logging as log


# 配置类
class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DATABASE_URL: str = "sqlite:///sqlite.db"
    LOG_LEVEL: str = "INFO"
    SQL_ECHO: bool = True
    RESOURCES_DIR_PATH: str = "resources"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 实例化配置
settings = Settings()

# 设置日志等级
log.basicConfig(level=settings.LOG_LEVEL)
