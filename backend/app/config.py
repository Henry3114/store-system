from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "小卖部销售管理系统"
    DEBUG: bool = True

    # 数据库配置（默认本地，生产环境用 Supabase）
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/store_system"

    # JWT 配置
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 小时

    # CORS 配置
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
