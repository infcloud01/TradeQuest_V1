import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # RPG Account Scaling System
    level = Column(Integer, default=1)
    level_profit = Column(Float, default=0.0)      
    total_profit = Column(Float, default=0.0)      
    current_title = Column(String, default="Apprentice Novice")
    allowed_lot_size = Column(Float, default=0.01)   
    
    # Core RPG Attributes (Scaled 1-100)
    discipline = Column(Integer, default=50)
    patience = Column(Integer, default=50)
    risk_management = Column(Integer, default=50)
    consistency = Column(Integer, default=50)

    trades = relationship("Trade", back_populates="owner")
    side_quests = relationship("SideQuest", back_populates="owner", cascade="all, delete-orphan")

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instrument = Column(String, nullable=False)
    lot_size = Column(Float, nullable=False)
    pnl = Column(Float, nullable=False)
    status = Column(String, default="closed")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="trades")

class SideQuest(Base):
    __tablename__ = "side_quests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    requirement = Column(String, nullable=False)
    quest_type = Column(String, nullable=False)    # e.g., 'half_lots', 'patience_win', 'streak'
    target_value = Column(Integer, nullable=False)  # Target condition count (e.g., 3 trades)
    current_value = Column(Integer, default=0)     # Current tracking value
    
    reward_stat = Column(String, nullable=False)   # Which stat gets boosted (e.g., 'discipline')
    reward_amount = Column(Integer, nullable=False) # Stat boost magnitude
    status = Column(String, default="IN PROGRESS") # IN PROGRESS, COMPLETED

    owner = relationship("User", back_populates="side_quests")