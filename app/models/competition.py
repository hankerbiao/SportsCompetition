from typing import List, Optional
from sqlmodel import Field, SQLModel


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
