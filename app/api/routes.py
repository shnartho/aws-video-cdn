from fastapi import APIRouter

from app.api.endpoints import videos

# Combine all API routers
router = APIRouter()
router.include_router(videos.router, prefix="/videos", tags=["videos"])
