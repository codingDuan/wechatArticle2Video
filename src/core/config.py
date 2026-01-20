import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # AWS S3 Configuration
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "digital-human-assets")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    # LLM Provider Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "gemini"

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_WHISPER_MODEL: str = os.getenv("OPENAI_WHISPER_MODEL", "whisper-1")
    OPENAI_FINETUNE_MODEL_ID: str = os.getenv("OPENAI_FINETUNE_MODEL_ID", "")



    class Config:
        case_sensitive = True

# Function to get settings, allowing for dynamic reloading of environment variables
def get_settings() -> Settings:
    return Settings()