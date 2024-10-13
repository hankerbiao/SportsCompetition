from fastapi import APIRouter

from .athlete import router

athlete_router = APIRouter()
athlete_router.include_router(router, tags=["运动员模块"])

__all__ = ["athlete_router"]
