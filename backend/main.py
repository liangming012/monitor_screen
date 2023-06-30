import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from api.v1 import login, users, projects, records, screens, shows, notices, healthy
from core.config import settings
# 不要使用以下代码自动创建数据库表，请使用 alembic的自动生成数据库迁移和迁移升级到最新版本命令
# from api.deps import engine
# from models.base import Base
# Base.metadata.create_all(bind=engine)
env = os.getenv('ENV')
if env == 'production':
    app = FastAPI(title=settings.PROJECT_NAME, docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
# 支持https请求
if settings.ENABLE_HTTPS:
    app.add_middleware(HTTPSRedirectMiddleware)
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(records.router, prefix="/records", tags=["records"])
api_router.include_router(screens.router, prefix="/screens", tags=["screens"])
api_router.include_router(shows.router, prefix="/shows", tags=["shows"])
api_router.include_router(notices.router, prefix="/notices", tags=["notices"])
api_router.include_router(healthy.router, prefix="/healthy", tags=["healthy"])
app.include_router(api_router, prefix=settings.API_V1_STR)
