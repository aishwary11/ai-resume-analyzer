from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    nvidia_api_key: str = Field(default="", repr=False)
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_model: str = "nvidia/nemotron-3.5-bolt-e4b"
    database_url: str = (
        "postgresql+asyncpg://postgres:aish@localhost:5432/resume_analyzer"
    )
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl_seconds: int = 900
    max_upload_mb: int = 8
    max_pdf_pages: int = 20
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", validate_default=True
    )

    @field_validator("nvidia_api_key")
    @classmethod
    def require_nvidia_api_key(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("NVIDIA_API_KEY must be configured.")
        return value


settings = Settings()
