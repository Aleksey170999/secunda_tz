from pydantic import BaseModel
from typing import Optional

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    level: int
    
    class Config:
        from_attributes = True
