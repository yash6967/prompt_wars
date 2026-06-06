from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ORMBase(BaseModel):
    class Config:
        from_attributes = True

class Token(ORMBase):
    access_token: str
    token_type: str

class TokenData(ORMBase):
    email: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    exam_target: Optional[str] = None
    exam_date: Optional[datetime] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(ORMBase):
    id: int
    name: str
    email: EmailStr
    exam_target: Optional[str]
    exam_date: Optional[datetime]
    created_at: datetime
    is_active: bool

class MoodCreate(BaseModel):
    mood_score: int
    emotion_tags: Optional[str] = None
    note: Optional[str] = None
    energy_level: Optional[int] = None
    sleep_hours: Optional[float] = None
    study_hours: Optional[float] = None

class MoodOut(ORMBase):
    id: int
    user_id: int
    mood_score: int
    emotion_tags: Optional[str]
    note: Optional[str]
    energy_level: Optional[int]
    sleep_hours: Optional[float]
    study_hours: Optional[float]
    logged_at: datetime

class AssessmentCreate(BaseModel):
    answers_json: str

class AssessmentOut(ORMBase):
    id: int
    user_id: int
    phq_score: int
    gad_score: int
    pss_score: int
    overall_level: str
    answers_json: str
    taken_at: datetime

class ActivityCreate(BaseModel):
    activity_type: str
    duration_minutes: int
    description: Optional[str] = None

class ActivityOut(ORMBase):
    id: int
    user_id: int
    activity_type: str
    duration_minutes: int
    description: Optional[str]
    logged_at: datetime

class AllyConnectionCreate(BaseModel):
    ally_name: str
    ally_email: EmailStr
    role: str

class AllyConnectionOut(ORMBase):
    id: int
    student_id: int
    ally_name: str
    ally_email: EmailStr
    role: str
    is_verified: bool
    created_at: datetime

class AllyNudgeOut(ORMBase):
    id: int
    connection_id: int
    generated_at: datetime
    insight_summary: str
    actionable_tip: str
    is_viewed: bool
