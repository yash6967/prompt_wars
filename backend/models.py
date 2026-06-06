import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    exam_target = Column(String, nullable=True)
    exam_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)

    moods = relationship("MoodEntry", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    allies = relationship("AllyConnection", back_populates="student", cascade="all, delete-orphan")

class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    mood_score = Column(Integer, nullable=False)
    emotion_tags = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    energy_level = Column(Integer, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    study_hours = Column(Float, nullable=True)
    logged_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    user = relationship("User", back_populates="moods")

class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    phq_score = Column(Integer, nullable=False)
    gad_score = Column(Integer, nullable=False)
    pss_score = Column(Integer, nullable=False)
    overall_level = Column(String, nullable=False)
    answers_json = Column(Text, nullable=True)
    taken_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    user = relationship("User", back_populates="assessments")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_type = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    logged_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    user = relationship("User", back_populates="activities")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    user = relationship("User", back_populates="messages")

class AllyConnection(Base):
    __tablename__ = "ally_connections"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    ally_name = Column(String, nullable=False)
    ally_email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    student = relationship("User", back_populates="allies")
    nudges = relationship("AllyNudge", back_populates="connection", cascade="all, delete-orphan")

class AllyNudge(Base):
    __tablename__ = "ally_nudges"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("ally_connections.id"), nullable=False, index=True)
    generated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)
    insight_summary = Column(Text, nullable=False)
    actionable_tip = Column(Text, nullable=False)
    is_viewed = Column(Boolean, default=False)

    connection = relationship("AllyConnection", back_populates="nudges")
