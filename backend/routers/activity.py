import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas, auth

router = APIRouter()

ADVICE_STRINGS = {
    "exercise": "Physically active breaks, even for 10 minutes, boost dopamine and reduce stress hormones.",
    "meditation": "Mindfulness and slow breathing lower your heart rate and bring cognitive clarity.",
    "social": "Talking with a supportive friend or family member releases oxytocin and buffers cortisol.",
    "hydration": "Dehydration leads to fatigue and loss of focus. Take a glass of water now!",
    "nap": "A power nap of 15-20 minutes can restore alertness without causing sleep inertia.",
    "hobbies": "Engaging in quick creative or recreation activities refreshes neural patterns."
}

@router.get("/advice")
def get_activity_advice(current_user: models.User = Depends(auth.get_current_user)):
    return ADVICE_STRINGS

@router.post("/log", response_model=schemas.ActivityOut)
def log_activity(
    activity_in: schemas.ActivityCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    new_log = models.ActivityLog(
        user_id=current_user.id,
        activity_type=activity_in.activity_type,
        duration_minutes=activity_in.duration_minutes,
        description=activity_in.description
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/today")
def get_today_activities(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    today_start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    activities = (
        db.query(models.ActivityLog)
        .filter(models.ActivityLog.user_id == current_user.id, models.ActivityLog.logged_at >= today_start)
        .all()
    )
    
    total_duration = sum(act.duration_minutes for act in activities)
    return {
        "activities": [
            {
                "id": act.id,
                "user_id": act.user_id,
                "activity_type": act.activity_type,
                "duration_minutes": act.duration_minutes,
                "description": act.description,
                "logged_at": act.logged_at
            }
            for act in activities
        ],
        "total_duration_minutes": total_duration,
        "count": len(activities)
    }
