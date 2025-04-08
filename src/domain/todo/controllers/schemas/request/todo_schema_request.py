import datetime

from pydantic import BaseModel, Field
from typing_extensions import Optional

from domain.todo.enums import TODOListStatusEnum


class TODOCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=255)
    expire_date: datetime.date
    status: TODOListStatusEnum
    _user: Optional[str]


class TODOUpdateRequest(BaseModel):
    title: str = Field(None, min_length=1, max_length=255)
    description: str = Field(None, min_length=1, max_length=255)
    expire_date: datetime.date = Field(None)
    status: TODOListStatusEnum = Field(None)
    _user: Optional[str]