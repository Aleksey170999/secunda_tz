from pydantic import BaseModel, model_validator
from typing import List, Optional
from .activity import Activity
from .building import Building

class OrganizationBase(BaseModel):
    name: str
    phone_numbers: List[str]
    building_id: int
    activity_ids: List[int] = []

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    building: "Building"
    activities: List["Activity"] = []

    @model_validator(mode='after')
    def fill_activity_ids(self):
        if self.activities:
            self.activity_ids = [activity.id for activity in self.activities]
        return self

    class Config:
        from_attributes = True

Organization.update_forward_refs()
