import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./store.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
