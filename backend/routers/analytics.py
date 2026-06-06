from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, auth
from backend.services import analytics_service

router = APIRouter()

@router.get("/summary")
def get_summary(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return analytics_service.calculate_wellness_summary(current_user.id, db)

@router.get("/escalation-check")
def escalation_check(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return analytics_service.check_escalation_risk(current_user.id, db)
