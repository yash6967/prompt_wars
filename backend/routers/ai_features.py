from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from backend.database import get_db
from backend import models, auth
from backend.services import ai_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.get("/story")
def get_story(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    latest_mood = (
        db.query(models.MoodEntry)
        .filter(models.MoodEntry.user_id == current_user.id)
        .order_by(models.MoodEntry.logged_at.desc())
        .first()
    )
    mood_score = latest_mood.mood_score if latest_mood else 5
    exam_target = current_user.exam_target or "upcoming exams"
    
    story = ai_service.generate_story(current_user.name, exam_target, mood_score)
    return {"story": story}

@router.post("/chat")
def chat(
    chat_req: ChatRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    user_msg = models.ChatMessage(
        user_id=current_user.id,
        role="user",
        content=chat_req.message
    )
    db.add(user_msg)
    db.commit()
    
    history_entries = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == current_user.id)
        .order_by(models.ChatMessage.sent_at.asc())
        .limit(20)
        .all()
    )
    
    history_list = [{"role": m.role, "content": m.content} for m in history_entries]
    
    reply = ai_service.chat_with_student(history_list, current_user.name)
    
    asst_msg = models.ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=reply
    )
    db.add(asst_msg)
    db.commit()
    
    return {"reply": reply}

@router.get("/chat/history")
def get_chat_history(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    history = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == current_user.id)
        .order_by(models.ChatMessage.sent_at.asc())
        .all()
    )
    return [{"role": m.role, "content": m.content} for m in history]

@router.get("/tip")
def get_tip(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    tips = [
        "Take a 5-minute break every 25 minutes of studying (Pomodoro method).",
        "Keep a water bottle on your desk. Staying hydrated keeps your brain active.",
        "Take 5 deep breaths if you start feeling overwhelmed by a study topic.",
        "Reward yourself with a short walk or light exercise after completing a study goal.",
        "Sleep is when memory consolidation happens. Don't skip on your 7-8 hours!"
    ]
    import random
    return {"tip": random.choice(tips)}

@router.get("/insight")
def get_insight(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    moods = (
        db.query(models.MoodEntry)
        .filter(models.MoodEntry.user_id == current_user.id)
        .order_by(models.MoodEntry.logged_at.desc())
        .limit(5)
        .all()
    )
    if not moods:
        return {"insight": "Start logging your daily mood to generate cognitive and study insights."}
        
    avg_mood = sum(m.mood_score for m in moods) / len(moods)
    if avg_mood < 5:
        insight = "Your recent logs show higher levels of exam stress. Focus on sleep and active recovery breaks."
    elif avg_mood < 8:
        insight = "You are maintaining a balanced mental state. Keep up the consistent check-ins."
    else:
        insight = "Excellent! You are feeling highly motivated and energized. Keep setting realistic study milestones."
        
    return {"insight": insight}
