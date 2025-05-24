from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    PROJECT_NAME: str = "AWS Video CDN"
    PROJECT_DESCRIPTION: str = "Video hosting service with AWS S3 and CloudFront CDN"
    PROJECT_VERSION: str = "0.1.0"
    
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # AWS Settings
    AWS_REGION: str = "eu-west-1"
    S3_BUCKET_NAME: str = "video-storage-bucket"
    CLOUDFRONT_DOMAIN: Optional[str] = None
    
    # Additional environment variables
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    HOST: str = "0.0.0.0"
    PORT: str = "8000"
    ENV: str = "development"
    LOG_LEVEL: str = "info"

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"  # Ignore extra fields from environment
    }


settings = Settings()
