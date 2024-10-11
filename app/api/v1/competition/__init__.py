from fastapi import APIRouter

from .team import router

team_router = APIRouter()
team_router.include_router(router, tags=["运动队模块"])

__all__ = ["team_router"]
