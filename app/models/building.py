from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    organizations = relationship("Organization", back_populates="building")

    def __repr__(self):
        return f"<Building {self.address}>"
