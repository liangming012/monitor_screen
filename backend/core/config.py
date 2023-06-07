import secrets
from typing import Any, Dict, List, Optional, Union

from dotenv import find_dotenv
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DOMAIN: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_NAME: str
    JENKINS_ACCOUNT: str
    JENKINS_PWD: str
    RECORD_SAVE_TIME: int

    class Config:
        case_sensitive = True
        env_file = find_dotenv("../../.env")


settings = Settings()




