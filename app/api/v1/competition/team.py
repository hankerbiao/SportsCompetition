import logging
from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from app.core.db import SessionDep
from app.models.competition import Team
from app.schemas.base import SuccessExtra
from app.utils.jwt import get_current_user_id

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="查看运动队列表")
async def list_team(
        db: SessionDep,
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        team_name: str = Query("", description="运动队名称，用于查询"),
):
    """
    查看指定运动队列表
    """
    query = select(Team)
    if team_name:
        query = query.where(Team.name.contains(team_name))

    offset = (page - 1) * page_size
    data = db.exec(query.offset(offset).limit(page_size)).all()

    # 将 Team 对象转换为字典
    serialized_data = [team.dict() for team in data]
    total = len(serialized_data)  # 获取总数
    return SuccessExtra(data=serialized_data, total=total, page=page, page_size=page_size)


@router.get("/all", summary="查看所有运动队列表")
async def list_all_teams(db: SessionDep):
    """
    查看所有运动队列表
    """
    user_id = get_current_user_id()
    print(user_id)
    data = db.exec(select(Team)).all()
    serialized_data = [team.dict() for team in data]
    return SuccessExtra(data=serialized_data)


@router.delete("/delete", summary="根据 ID 删除运动队")
async def delete_team(id: int, db: SessionDep):
    """
    根据 ID 删除运动队
    """
    team = db.get(Team, id)
    if not team:
        raise HTTPException(status_code=404, detail="运动队未找到")

    db.delete(team)
    db.commit()
    return SuccessExtra(data={"message": "运动队已删除"})


@router.put("/update", summary="根据 ID 修改运动队信息")
async def update_team(id: int, updated_team: Team, db: SessionDep):
    """
    根据 ID 修改运动队信息
    """
    # 查询指定 ID 的运动队
    team = db.get(Team, id)
    if not team:
        raise HTTPException(status_code=404, detail="运动队未找到")

    # 更新运动队信息
    team.name = updated_team.name
    team.short_name = updated_team.short_name
    team.address = updated_team.address
    team.leader_name = updated_team.leader_name
    team.leader_phone = updated_team.leader_phone
    team.leader_photo = updated_team.leader_photo
    team.doctor_name = updated_team.doctor_name
    team.doctor_phone = updated_team.doctor_phone
    team.staff_name = updated_team.staff_name
    team.staff_phone = updated_team.staff_phone
    team.coaches = updated_team.coaches

    # 提交更改
    db.add(team)
    db.commit()

    return SuccessExtra(data={"message": "运动队信息已更新"})


@router.post("/create", summary="增加运动队")
async def add_team(new_team: Team, db: SessionDep):
    """
    增加运动队
    """
    db.add(new_team)
    db.commit()
    return SuccessExtra(data={"message": "运动队已添加", "team_id": new_team.id})
