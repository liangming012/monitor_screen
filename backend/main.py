from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter

from api.deps import engine
from api.v1 import login, users, projects, records, screens, shows, notices, watch_notices
from core.config import settings
from models.base import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

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
api_router.include_router(watch_notices.router, prefix="/watch_notices", tags=["watch_notices"])
app.include_router(api_router, prefix=settings.API_V1_STR)
