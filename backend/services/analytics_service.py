from sqlalchemy.orm import Session
from backend import models

def calculate_wellness_summary(user_id: int, db: Session) -> dict:
    moods = db.query(models.MoodEntry).filter(models.MoodEntry.user_id == user_id).order_by(models.MoodEntry.logged_at.desc()).limit(14).all()
    latest_assessment = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user_id).order_by(models.AssessmentResult.taken_at.desc()).first()
    
    avg_mood = sum(m.mood_score for m in moods) / len(moods) if moods else 0.0
    avg_energy = sum(m.energy_level for m in moods if m.energy_level is not None) / len([m for m in moods if m.energy_level is not None]) if any(m.energy_level is not None for m in moods) else 0.0
    avg_sleep = sum(m.sleep_hours for m in moods if m.sleep_hours is not None) / len([m for m in moods if m.sleep_hours is not None]) if any(m.sleep_hours is not None for m in moods) else 0.0
    avg_study = sum(m.study_hours for m in moods if m.study_hours is not None) / len([m for m in moods if m.study_hours is not None]) if any(m.study_hours is not None for m in moods) else 0.0
    
    return {
        "avg_mood_14d": round(avg_mood, 2),
        "avg_energy_14d": round(avg_energy, 2),
        "avg_sleep_14d": round(avg_sleep, 2),
        "avg_study_14d": round(avg_study, 2),
        "total_mood_logs": len(moods),
        "latest_stress_level": latest_assessment.overall_level if latest_assessment else "none",
        "latest_phq_score": latest_assessment.phq_score if latest_assessment else 0,
        "latest_gad_score": latest_assessment.gad_score if latest_assessment else 0,
        "latest_pss_score": latest_assessment.pss_score if latest_assessment else 0,
    }

def check_escalation_risk(user_id: int, db: Session) -> dict:
    moods = db.query(models.MoodEntry).filter(models.MoodEntry.user_id == user_id).order_by(models.MoodEntry.logged_at.desc()).limit(3).all()
    latest_assessment = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user_id).order_by(models.AssessmentResult.taken_at.desc()).first()
    
    trigger_escalation = False
    reasons = []
    
    if latest_assessment:
        if latest_assessment.phq_score >= 15:
            trigger_escalation = True
            reasons.append("Severe PHQ-9 (depression) score detected")
        if latest_assessment.gad_score >= 15:
            trigger_escalation = True
            reasons.append("Severe GAD-7 (anxiety) score detected")
        if latest_assessment.pss_score >= 11:
            trigger_escalation = True
            reasons.append("Severe PSS-4 (stress) score detected")
            
    if moods:
        avg_mood_recent = sum(m.mood_score for m in moods) / len(moods)
        if avg_mood_recent <= 3.0:
            trigger_escalation = True
            reasons.append(f"Extremely low average mood ({avg_mood_recent:.1f}/10) over recent logs")
            
    return {
        "escalation_required": trigger_escalation,
        "reasons": reasons,
        "support_helplines": [
            {"name": "AASRA (Suicide Prevention)", "contact": "91-9820466726"},
            {"name": "Kiran Mental Health Helpline", "contact": "1800-599-0019"},
            {"name": "Vandrevala Foundation", "contact": "+91 9999 666 555"}
        ]
    }
