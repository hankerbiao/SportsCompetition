import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.db import SessionDep
from app.models.competition import Event
from app.schemas import SuccessExtra

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/create", summary="创建赛事")
def create_event(event: Event, db: SessionDep):
    db_event = Event.model_validate(event)
    timestamp_ms = db_event.date
    # 将时间戳转换为秒
    timestamp_s = timestamp_ms / 1000
    date_time = datetime.fromtimestamp(timestamp_s)
    formatted_date = date_time.strftime('%Y-%m-%d')
    db_event.date = formatted_date
    db.add(db_event)
    db.commit()
    return SuccessExtra()


@router.get("/list", summary="列出所有赛事情况")
def read_events(
        db: SessionDep,
        page: int = 0,
        page_size: int = 100,
):
    events = db.exec(select(Event)).all()
    print(events)
    serialized_data = [event.dict() for event in events]
    total = len(serialized_data)  # 获取总数
    return SuccessExtra(data=serialized_data, total=total, page=page, page_size=page_size)


#
#
# @router.get("/{event_id}", response_model=Event)
# def read_event(event_id: int, db: SessionDep):
#     event = db.get(Event, event_id)
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found")
#     return event
#
#
# @router.put("/{event_id}", response_model=Event)
# def update_event(
#         event_id: int,
#         event_update: Event,
#         db: SessionDep
# ):
#     db_event = db.get(Event, event_id)
#     if not db_event:
#         raise HTTPException(status_code=404, detail="Event not found")
#
#     event_data = event_update.model_dump(exclude_unset=True)
#     for key, value in event_data.items():
#         setattr(db_event, key, value)
#
#     db.add(db_event)
#     db.commit()
#     db.refresh(db_event)
#     return db_event
#
#
@router.delete("/delete", summary="删除赛事")
def delete_event(id: int, db: SessionDep):
    event = db.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return SuccessExtra()
