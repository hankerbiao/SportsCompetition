from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum


class Team(SQLModel, table=True):
    __tablename__ = "team"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    name: str = Field(index=True)
    short_name: str
    address: str
    leader_name: str
    leader_phone: str
    leader_photo: str
    doctor_name: str
    doctor_phone: str
    staff_name: str
    staff_phone: str
    coaches1: str
    coaches2: Optional[str] = None
    coaches1_phone: str
    coaches2_phone: Optional[str] = None


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


class EventStatus(str, Enum):
    UPCOMING = "即将开始"
    ONGOING = "进行中"
    COMPLETED = "已结束"
    CANCELLED = "已取消"


class Event(SQLModel, table=True):
    __tablename__ = "event"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100, index=True, description="赛事名称")
    status: EventStatus = Field(..., description="赛事状态")
    address: str = Field(..., max_length=200, description="比赛地址")
    date: str = Field(..., description="比赛日期")
    participants: int = Field(..., ge=0, description="报名人数")
