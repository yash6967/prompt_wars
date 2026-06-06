from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import models, schemas, auth
from backend.services import ai_service

router = APIRouter()

@router.post("/invite", response_model=schemas.AllyConnectionOut)
def invite_ally(
    ally_in: schemas.AllyConnectionCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(models.AllyConnection).filter(
        models.AllyConnection.student_id == current_user.id,
        models.AllyConnection.ally_email == ally_in.ally_email
    ).first()
    
    if existing:
        return existing
        
    new_conn = models.AllyConnection(
        student_id=current_user.id,
        ally_name=ally_in.ally_name,
        ally_email=ally_in.ally_email,
        role=ally_in.role,
        is_verified=True
    )
    db.add(new_conn)
    db.commit()
    db.refresh(new_conn)
    return new_conn

@router.get("/connections", response_model=List[schemas.AllyConnectionOut])
def get_connections(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.AllyConnection).filter(models.AllyConnection.student_id == current_user.id).all()

@router.get("/nudges", response_model=List[schemas.AllyNudgeOut])
def get_nudges(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    connections = db.query(models.AllyConnection).filter(models.AllyConnection.student_id == current_user.id).all()
    if not connections:
        return []
        
    moods = db.query(models.MoodEntry).filter(models.MoodEntry.user_id == current_user.id).all()
    if not moods:
        avg_mood = 7.0
        avg_energy = 7.0
        recent_note = "Feeling okay."
    else:
        avg_mood = sum(m.mood_score for m in moods) / len(moods)
        avg_energy = sum(m.energy_level if m.energy_level is not None else 5 for m in moods) / len(moods)
        recent_note = moods[-1].note or ""

    nudges_out = []
    for conn in connections:
        nudge_text = ai_service.generate_subtle_ally_nudge(current_user.name, avg_mood, avg_energy, recent_note)
        
        if "Actionable Tips:" in nudge_text:
            parts = nudge_text.split("Actionable Tips:")
            insight = parts[0].strip()
            tip = parts[1].strip()
        else:
            insight = "Student wellness overview generated."
            tip = nudge_text
            
        nudge = models.AllyNudge(
            connection_id=conn.id,
            insight_summary=insight,
            actionable_tip=tip,
            is_viewed=False
        )
        db.add(nudge)
        db.commit()
        db.refresh(nudge)
        nudges_out.append(nudge)
        
    return nudges_out
