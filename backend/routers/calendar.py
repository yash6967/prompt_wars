import os
import json
import datetime
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from backend import models, auth

router = APIRouter()

EXAMS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "exams.json")

def load_exams():
    if not os.path.exists(EXAMS_FILE):
        return []
    with open(EXAMS_FILE, "r") as f:
        return json.load(f)

@router.get("/exams")
def get_exams(
    current_user: models.User = Depends(auth.get_current_user)
):
    return load_exams()

@router.get("/upcoming")
def get_upcoming_exams(
    days: int = Query(120),
    current_user: models.User = Depends(auth.get_current_user)
):
    exams = load_exams()
    upcoming = []
    now = datetime.datetime.utcnow()
    limit_date = now + datetime.timedelta(days=days)
    
    for exam in exams:
        try:
            exam_date = datetime.datetime.fromisoformat(exam["date"])
            if now <= exam_date <= limit_date:
                upcoming.append(exam)
        except Exception:
            continue
            
    return upcoming
