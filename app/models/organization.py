from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.base import Base

organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phone_numbers = Column(ARRAY(String), nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=False)
    
    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity, back_populates="organizations")

    def __repr__(self):
        return f"<Organization {self.name}>"
