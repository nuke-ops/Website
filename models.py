from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class Dice(Base):
    __tablename__ = "Dice"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    dice = Column(Integer, nullable=False)
    sides = Column(Integer, nullable=False)
    throws = Column(String(255), nullable=False)
    sum = Column(Integer, nullable=False)
    modifier = Column(String(255), default="", nullable=True)
    date = Column(DateTime, default=func.now())
