import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import models, schemas, auth

router = APIRouter()

QUESTIONS = [
    {"id": 1, "text": "Little interest or pleasure in doing things?", "category": "PHQ"},
    {"id": 2, "text": "Feeling down, depressed, or hopeless?", "category": "PHQ"},
    {"id": 3, "text": "Trouble falling or staying asleep, or sleeping too much?", "category": "PHQ"},
    {"id": 4, "text": "Feeling tired or having little energy?", "category": "PHQ"},
    {"id": 5, "text": "Poor appetite or overeating?", "category": "PHQ"},
    {"id": 6, "text": "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?", "category": "PHQ"},
    {"id": 7, "text": "Trouble concentrating on things, such as reading or watching television?", "category": "PHQ"},
    {"id": 8, "text": "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual?", "category": "PHQ"},
    {"id": 9, "text": "Thoughts that you would be better off dead, or of hurting yourself in some way?", "category": "PHQ"},
    {"id": 10, "text": "Feeling nervous, anxious or on edge?", "category": "GAD"},
    {"id": 11, "text": "Not being able to stop or control worrying?", "category": "GAD"},
    {"id": 12, "text": "Worrying too much about different things?", "category": "GAD"},
    {"id": 13, "text": "Trouble relaxing?", "category": "GAD"},
    {"id": 14, "text": "Being so restless that it is hard to sit still?", "category": "GAD"},
    {"id": 15, "text": "Becoming easily annoyed or irritable?", "category": "GAD"},
    {"id": 16, "text": "Feeling afraid as if something awful might happen?", "category": "GAD"},
    {"id": 17, "text": "In the last month, how often have you felt that you were unable to control the important things in your life?", "category": "PSS"},
    {"id": 18, "text": "In the last month, how often have you felt confident about your ability to handle your personal problems?", "category": "PSS", "reverse": True},
    {"id": 19, "text": "In the last month, how often have you felt that things were going your way?", "category": "PSS", "reverse": True},
    {"id": 20, "text": "In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?", "category": "PSS"}
]

@router.get("/questions")
def get_questions(current_user: models.User = Depends(auth.get_current_user)):
    return QUESTIONS

@router.post("/", response_model=schemas.AssessmentOut)
def submit_assessment(
    assessment_in: schemas.AssessmentCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    try:
        answers = json.loads(assessment_in.answers_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid answers_json format")
        
    phq_score = 0
    gad_score = 0
    pss_score = 0
    
    for q in QUESTIONS:
        q_id_str = str(q["id"])
        score = answers.get(q_id_str, 0)
        if not (0 <= score <= 3):
            score = 0
            
        if q["category"] == "PHQ":
            phq_score += score
        elif q["category"] == "GAD":
            gad_score += score
        elif q["category"] == "PSS":
            if q.get("reverse"):
                pss_score += (3 - score)
            else:
                pss_score += score
                
    if phq_score >= 15 or gad_score >= 15 or pss_score >= 11:
        overall_level = "severe"
    elif phq_score >= 10 or gad_score >= 10 or pss_score >= 7:
        overall_level = "moderate"
    else:
        overall_level = "mild"
        
    new_result = models.AssessmentResult(
        user_id=current_user.id,
        phq_score=phq_score,
        gad_score=gad_score,
        pss_score=pss_score,
        overall_level=overall_level,
        answers_json=assessment_in.answers_json,
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result
