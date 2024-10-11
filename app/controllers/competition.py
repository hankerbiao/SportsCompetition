from typing import List, Dict

from app.core.crud import CRUDBase
from app.models.competition import Team
from app.schemas.competition import TeamCreate, TeamUpdate


class TeamController(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def __init__(self):
        super().__init__(model=Team)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()

    async def get_team_with_coaches(self, team_id: int) -> Dict:
        team = await self.get(id=team_id)
        return {
            "id": team.id,
            "name": team.name,
            "short_name": team.short_name,
            "address": team.address,
            "leader_name": team.leader_name,
            "leader_phone": team.leader_phone,
            "leader_photo": team.leader_photo,
            "doctor_name": team.doctor_name,
            "doctor_phone": team.doctor_phone,
            "staff_name": team.staff_name,
            "staff_phone": team.staff_phone,
            "coaches": team.coaches_list
        }


team_controller = TeamController()
