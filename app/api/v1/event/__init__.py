from fastapi import APIRouter

from .event import router

event_router = APIRouter()
event_router.include_router(router, tags=["赛事模块"])

__all__ = ["event_router"]
