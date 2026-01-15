from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('activities.id'), nullable=True)
    level = Column(Integer, default=1, nullable=False)
    
    children = relationship("Activity", 
                          backref='parent', 
                          remote_side=[id],
                          cascade="all")
    
    organizations = relationship("Organization", 
                               secondary='organization_activity', 
                               back_populates="activities")

    def __repr__(self):
        return f"<Activity {self.name}>"
