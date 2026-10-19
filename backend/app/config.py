import os

PORT = int(os.getenv("PORT", 8000))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyberdoom.db")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
