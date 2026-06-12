from pydantic import BaseModel
from datetime import datetime

class TradeCreate(BaseModel):
    instrument: str
    lot_size: float
    pnl: float

class TradeResponse(TradeCreate):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class SideQuestResponse(BaseModel):
    id: int
    title: str
    requirement: str
    quest_type: str
    target_value: int
    current_value: int
    reward_stat: str
    reward_amount: int
    status: str
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    level: int
    level_profit: float
    total_profit: float
    current_title: str
    allowed_lot_size: float
    discipline: int
    patience: int
    risk_management: int
    consistency: int
    class Config:
        from_attributes = True