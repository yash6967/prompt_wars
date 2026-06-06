from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth_router, mood, assessment, ai_features, calendar, activity, analytics, ally

app = FastAPI(title="Saathi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(mood.router, prefix="/mood", tags=["mood"])
app.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
app.include_router(ai_features.router, prefix="/ai", tags=["ai"])
app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
app.include_router(activity.router, prefix="/activity", tags=["activity"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(ally.router, prefix="/ally", tags=["ally"])

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Saathi"}
