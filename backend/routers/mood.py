import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend import models, schemas, auth

router = APIRouter()

@router.post("/", response_model=schemas.MoodOut)
def create_mood(
    mood_in: schemas.MoodCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    new_entry = models.MoodEntry(
        user_id=current_user.id,
        mood_score=mood_in.mood_score,
        emotion_tags=mood_in.emotion_tags,
        note=mood_in.note,
        energy_level=mood_in.energy_level,
        sleep_hours=mood_in.sleep_hours,
        study_hours=mood_in.study_hours,
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/history", response_model=List[schemas.MoodOut])
def get_mood_history(
    days: Optional[int] = None,
    limit: int = 100,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(models.MoodEntry).filter(models.MoodEntry.user_id == current_user.id)
    if days is not None:
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        query = query.filter(models.MoodEntry.logged_at >= start_date)
    return query.order_by(models.MoodEntry.logged_at.desc()).limit(limit).all()

@router.get("/today", response_model=Optional[schemas.MoodOut])
def get_today_mood(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    today_start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    return (
        db.query(models.MoodEntry)
        .filter(models.MoodEntry.user_id == current_user.id, models.MoodEntry.logged_at >= today_start)
        .order_by(models.MoodEntry.logged_at.desc())
        .first()
    )
