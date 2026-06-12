import os
import datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from . import models, schemas

# Initialize database tables on application boot
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TradeQuest RPG Engine", version="2.0.0")


def spawn_all_ai_quests(user_id: int, db: Session):
    """The AI Spawner Brain: Scans all quest categories and ensures the trader

    always has a full board of 4 active behavioral missions simultaneously.
    """
    active_quests = db.query(models.SideQuest).filter(
        models.SideQuest.user_id == user_id, 
        models.SideQuest.status == "IN PROGRESS"
    ).all()
    
    active_types = [q.quest_type for q in active_quests]

    # Category 1: Discipline Quest Check
    if "under_leverage" not in active_types:
        db.add(models.SideQuest(
            user_id=user_id,
            title="🛡️ Tactical Restraint",
            requirement="Log 2 trades using strictly less than your max allowed lot size.",
            quest_type="under_leverage",
            target_value=2,
            reward_stat="discipline",
            reward_amount=10
        ))

    # Category 2: Patience Quest Check
    if "patience_win" not in active_types:
        db.add(models.SideQuest(
            user_id=user_id,
            title="⏳ Diamond Hands Quest",
            requirement="Secure 2 consecutive trades with a profit greater than $25.00.",
            quest_type="patience_win",
            target_value=2,
            reward_stat="patience",
            reward_amount=10
        ))

    # Category 3: Risk Management Quest Check
    if "safe_tier" not in active_types:
        db.add(models.SideQuest(
            user_id=user_id,
            title="🧱 Iron Bastion",
            requirement="Successfully log 3 trades without dropping back a tier level.",
            quest_type="safe_tier",
            target_value=3,
            reward_stat="risk_management",
            reward_amount=10
        ))

    # Category 4: Consistency Quest Check
    if "win_streak" not in active_types:
        db.add(models.SideQuest(
            user_id=user_id,
            title="🎯 Rhythm Calibrator",
            requirement="Achieve a clean 2-trade winning streak right now.",
            quest_type="win_streak",
            target_value=2,
            reward_stat="consistency",
            reward_amount=10
        ))

    db.commit()


# ─── USER PROFILE ROUTES ──────────────────────────────────────────────────────

@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        spawn_all_ai_quests(db_user.id, db)
        return db_user
    
    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    spawn_all_ai_quests(new_user.id, db)
    return new_user


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Trader not found")
    return user


# ─── CORE ACCOUNT SYSTEM & LOG LOOPS ──────────────────────────────────────────

@app.get("/users/{user_id}/trades", response_model=List[schemas.TradeResponse])
def get_user_trades(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.user_id == user_id).order_by(models.Trade.created_at.desc()).all()


@app.post("/trades/", response_model=schemas.TradeResponse, status_code=status.HTTP_201_CREATED)
def log_trade(trade: schemas.TradeCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Trader profile not found")
    
    # Enforce Lot Sizing Sifter
    if trade.lot_size > user.allowed_lot_size:
        raise HTTPException(
            status_code=400, 
            detail=f"Quest Violation! Your tier limits you to a max lot size of {user.allowed_lot_size}."
        )

    new_trade = models.Trade(**trade.model_dump(), user_id=user_id)
    db.add(new_trade)
    db.flush()

    # --- EXPERT ATTRIBUTE MODIFIER CALCULATIONS ---
    if trade.lot_size < user.allowed_lot_size:
        user.discipline += 4
    else:
        user.discipline -= 2
        
    level_target = user.level * 50.0
    if trade.pnl < 0:
        if (abs(trade.pnl) / level_target) > 0.25:
            user.risk_management -= 15
        else:
            user.risk_management += 2
    else:
        user.risk_management += 1

    history = db.query(models.Trade).filter(models.Trade.user_id == user_id).order_by(models.Trade.created_at.desc()).all()
    recent_trades = history[:5]
    win_streak, loss_streak = 0, 0
    for t in recent_trades:
        if t.pnl >= 0:
            if loss_streak > 0: break
            win_streak += 1
        else:
            if win_streak > 0: break
            loss_streak += 1
            
    if win_streak >= 3: user.consistency += 5
    elif loss_streak >= 3: user.consistency -= 5

    wins = [t.pnl for t in history if t.pnl > 0]
    losses = [abs(t.pnl) for t in history if t.pnl < 0]
    avg_win = sum(wins) / len(wins) if wins else 1.0
    avg_loss = sum(losses) / len(losses) if losses else 1.0
    if (avg_win / avg_loss) >= 2.0: user.patience += 6
    elif (avg_win / avg_loss) < 1.0: user.patience -= 4

    user.discipline = max(1, min(100, user.discipline))
    user.risk_management = max(1, min(100, user.risk_management))
    user.consistency = max(1, min(100, user.consistency))
    user.patience = max(1, min(100, user.patience))

    # --- SIDE QUESTS EVALUATOR ENGINE ---
    active_quests = db.query(models.SideQuest).filter(
        models.SideQuest.user_id == user_id, 
        models.SideQuest.status == "IN PROGRESS"
    ).all()

    for active_quest in active_quests:
        quest_triggered = False
        if active_quest.quest_type == "under_leverage" and trade.lot_size < user.allowed_lot_size:
            quest_triggered = True
        elif active_quest.quest_type == "patience_win" and trade.pnl >= 25.0:
            quest_triggered = True
        elif active_quest.quest_type == "safe_tier" and trade.pnl >= -10.0:
            quest_triggered = True
        elif active_quest.quest_type == "win_streak" and trade.pnl > 0:
            quest_triggered = True
            
        if quest_triggered:
            active_quest.current_value += 1
            if active_quest.current_value >= active_quest.target_value:
                active_quest.status = "COMPLETED"
                current_stat_val = getattr(user, active_quest.reward_stat)
                setattr(user, active_quest.reward_stat, min(100, current_stat_val + active_quest.reward_amount))

    # --- SCALING HARD BREAK PROGRESSION METRICS ---
    user.total_profit += trade.pnl
    user.level_profit += trade.pnl
    
    if user.level_profit >= level_target:
        user.level_profit = 0.0  # Reset progress to 0 on level up
        user.level += 1
        user.allowed_lot_size = round(user.level * 0.01, 2)
    elif user.level_profit < 0 and user.level > 1:
        user.level -= 1
        user.allowed_lot_size = round(user.level * 0.01, 2)
        user.level_profit = (user.level * 50.0) + user.level_profit

    # Title Rank Adjustments
    if user.level == 1: user.current_title = "Apprentice Novice"
    elif user.level == 2: user.current_title = "Market Mountaineer"
    elif user.level == 3: user.current_title = "Trend Tactician"
    elif user.level == 4: user.current_title = "Citadel Fund Manager"
    elif user.level == 5: user.current_title = "Prop Firm Gladiator"
    else: user.current_title = f"Legend Arena Sovereign (Tier {user.level - 5})"
        
    db.commit()
    
    # Top off side quests array board
    spawn_all_ai_quests(user_id, db)
        
    return new_trade


# ─── COACH GUIDANCE RETRIEVAL ─────────────────────────────────────────────────

@app.get("/users/{user_id}/coach-review")
def get_coach_review(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user: raise HTTPException(status_code=44, detail="Trader profile not found")
        
    evaluation = "I am watching your chart deployments closely, student. Proceed with your training."
    advice = "Execute trades inside your allowed lot parameters to gather initial performance data."
    archetype = "Sage Mentor"

    if user.discipline < 45:
        archetype = "Disciplinarian"
        evaluation = "You are treating your account scaling plan like a casino floor. You are maxing out your lot size limit on nearly every execution."
        advice = "Take your next 2 trades at half of your maximum allowed lot size. Prove you govern the market, not your impulses."
    elif user.patience < 45:
        archetype = "Risk Strategist"
        evaluation = "Your data indicates a heavy win-cutting habit. You panic and secure tiny profits early, but you let your losing positions float into deep drawdowns."
        advice = "Set a strict Take-Profit target on your next trade and do not click close manually. Force yourself to sit on your hands."
    elif user.risk_management < 40:
        archetype = "Shield Master"
        evaluation = "A massive catastrophe hit your portfolio. Your risk scores plummeted because you allowed a single bad trade to devastate your current tier's progress."
        advice = "Accepting a small loss is a defensive victory. Cut your next losing trade immediately when it violates your setup validation rules."
    elif user.consistency > 65:
        archetype = "Grandmaster"
        evaluation = "Phenomenal execution string! Your multi-trade win streak shows immense mechanical alignment and technical composure."
        advice = "Pride comes before a margin call. Do not increase your sizing out of overconfidence; stay sharp on your current level quest."

    return {
        "coach_name": "Jesse",  # Updated name in honor of Jesse Livermore
        "archetype": archetype, 
        "evaluation": evaluation, 
        "advice": advice
    }


@app.get("/users/{user_id}/side-quests", response_model=List[schemas.SideQuestResponse])
def get_side_quests(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.SideQuest).filter(models.SideQuest.user_id == user_id).order_by(models.SideQuest.id.desc()).all()


# ─── STATIC DESKTOP FILES SERVING ROUTE ────────────────────────────────────────

CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
UI_DIR = os.path.join(CURRENT_DIR, "ui")

@app.get("/play")
def play_game():
    return FileResponse(os.path.join(UI_DIR, "index.html"))