from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    name: str = Field(max_length=100)
    short_name: str = Field(max_length=50)
    address: str
    leader_name: str = Field(max_length=100)
    leader_phone: str = Field(max_length=20)
    leader_photo: str = Field()
    doctor_name: Optional[str] = Field(default=None, max_length=100)  # 允许为空
    doctor_phone: Optional[str] = Field(default=None, max_length=20)  # 允许为空
    staff_name: str = Field(max_length=100)
    staff_phone: str = Field(max_length=20)
    coaches1: str = Field()  # 教练1
    coaches1_phone: str = Field()  # 教练1电话
    coaches2: Optional[str] = Field(default=None)  # 允许为空的教练2
    coaches2_phone: Optional[str] = Field(default=None)  # 允许为空的教练2电话

    def __str__(self):
        return self.name


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    username: str = Field(..., max_length=20, unique=True, index=True)
    alias: Optional[str] = Field(default=None, max_length=30)
    email: str = Field(..., max_length=255, unique=True, index=True)
    phone: Optional[str] = Field(default=None, max_length=20)
    password: Optional[str] = Field(default=None, max_length=128)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    last_login: Optional[datetime] = Field(default=None)
    dept_id: Optional[int] = Field(default=None)

    athletes: List["Athlete"] = Relationship(back_populates="user")



class Athlete(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    name: str = Field(..., index=True)
    id_card: str = Field(..., unique=True)
    gender: str
    kumite_group: Optional[str] = Field(default=None)
    kata_group: Optional[str] = Field(default=None)
    individual_kumite: Optional[str] = Field(default=None)
    individual_kata: Optional[str] = Field(default=None)
    pair_kata: Optional[str] = Field(default=None)
    team_kata: Optional[str] = Field(default=None)
    mixed_pair_kata: Optional[str] = Field(default=None)
    team_kumite: Optional[str] = Field(default=None)
    multi_team_free_kata: Optional[str] = Field(default=None)
    mixed_team_kata: Optional[str] = Field(default=None)
    # fee: Optional[str] = Field(default=None)

    user: Optional[User] = Relationship(back_populates="athletes")
