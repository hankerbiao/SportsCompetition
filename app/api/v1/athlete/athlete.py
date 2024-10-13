import logging
from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from app.core.ctx import CTX_USER_ID
from app.core.db import SessionDep
from app.models.competition import Athlete, User
from app.schemas.base import SuccessExtra

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="查看运动员列表")
async def list_team(
        db: SessionDep,
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        name: str = Query("", description="运动员名称，用于查询"),
):
    """
    查看指定运动员列表
    """
    user_id = CTX_USER_ID.get()
    if user_id == 1:
        query = select(Athlete)
    else:
        query = select(Athlete).where(Athlete.user_id == user_id)
    if name:
        query = query.where(Athlete.name == name.strip())
    offset = (page - 1) * page_size
    data = db.exec(query.offset(offset).limit(page_size)).all()

    # 将 Athlete 对象转换为字典
    serialized_data = [team.dict() for team in data]
    total = len(serialized_data)  # 获取总数
    return SuccessExtra(data=serialized_data, total=total, page=page, page_size=page_size)


@router.delete("/delete", summary="根据 ID 删除运动员")
async def delete_athlete(id: int, db: SessionDep):
    """
    根据 ID 删除运动员
    """
    team = db.get(Athlete, id)
    if not team:
        raise HTTPException(status_code=404, detail="运动员未找到")

    db.delete(team)
    db.commit()
    return SuccessExtra(data={"message": "运动员已删除"})


@router.post("/create", summary="增加运动员")
def create_athlete(
        athlete: Athlete,
        db: SessionDep
):
    user_id = CTX_USER_ID.get()
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 运动员唯一
    db_athlete = db.exec(select(Athlete).where(Athlete.id_card == athlete.id_card)).first()
    if db_athlete:
        raise HTTPException(status_code=400, detail=f"运动员{athlete.id_card}已存在")

    athlete.user_id = user_id
    db.add(athlete)
    db.commit()
    db.refresh(athlete)
    return SuccessExtra(data={"message": "创建成功"})
