# ================================================================================
# SAATHI — Student Mental Wellness Tracker (Agent-Ready Production Blueprint)
# Target Stack: Python 3.11+, FastAPI, Uvicorn, Streamlit, SQLite, SQLAlchemy, Anthropic
# Mode: Automated Long-Running Agent Loop (Ralph Wiggum Schema)
# ================================================================================

=== PHASE 1: SYSTEM ENVIRONMENT & SCRATCHPAD CONFIGURATION ===

TASK-001: Structural Directory Scaffolding
DESCRIPTION: Build the fundamental repository folder tree layout for decoupled back-end and front-end microservices.
STEPS:
  - Create root subdirectories: `backend/routers`, `backend/services`, `frontend/utils`, `frontend/pages`, and `data`.
  - Create empty operational initialization anchors: `backend/__init__.py`, `backend/routers/__init__.py`, `backend/services/__init__.py`, and `frontend/utils/__init__.py`.
  - Write a root level `.gitignore` containing exactly:
    venv/
    __pycache__/
    *.db
    .env
    .DS_Store
VALIDATION: Execute shell script line `ls -R backend frontend data` and verify all target directories exist with their corresponding init anchors.
STATUS: TODO

TASK-002: Pinning and Installing Dependencies
DESCRIPTION: Provision the virtual execution runtime workspace with explicit version-locked software modules.
STEPS:
  - Create a root-level file named `requirements.txt` containing the following exact layout:
    fastapi==0.115.5
    uvicorn[standard]==0.32.1
    sqlalchemy==2.0.36
    python-jose[cryptography]==3.3.0
    passlib[bcrypt]==1.7.4
    python-dotenv==1.0.1
    anthropic==0.40.0
    httpx==0.28.0
    streamlit==1.40.2
    plotly==5.24.1
    pandas==2.2.3
    apscheduler==3.10.4
    pydantic-settings==2.6.1
    pydantic==2.10.3
    email-validator==2.2.0
  - Run terminal command: `pip install -r requirements.txt`
VALIDATION: Run command `python -c "import fastapi, streamlit, anthropic, sqlalchemy, jose, passlib; print('ENV_SUCCESS')"` and verify output matches 'ENV_SUCCESS'.
STATUS: TODO

TASK-003: Core Architecture Configuration Manager
DESCRIPTION: Centralize runtime operational secrets, access policies, and file pathways using strict configuration settings types.
STEPS:
  - Create a deployment template file named `.env.example` containing:
    SECRET_KEY=your-super-secret-jwt-key-change-this
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=10080
    DATABASE_URL=sqlite:///./data/saathi.db
    ANTHROPIC_API_KEY=sk-ant-...
    BACKEND_URL=http://localhost:8000
  - Duplicate `.env.example` into a production tracking destination file named `.env`.
  - Create the parsing engine script `backend/config.py` using Pydantic BaseSettings:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        SECRET_KEY: str = "change-me"
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
        DATABASE_URL: str = "sqlite:///./data/saathi.db"
        ANTHROPIC_API_KEY: str = ""
        BACKEND_URL: str = "http://localhost:8000"
        class Config:
            env_file = ".env"
    settings = Settings()
VALIDATION: Run command `python -c "from backend.config import settings; print(settings.ALGORITHM)"` and confirm the configuration manager parses strings matching 'HS256'.
STATUS: TODO

TASK-004: Engine Connection Setup and Complete ORM Data Models
DESCRIPTION: Design data engine frameworks using file-based persistent SQLite schemas mapping telemetry, tracking variables, and parent ally connection tables.
STEPS:
  - Create `backend/database.py` initializing create_engine configs with SQLite multithread processing flags, establishing SessionLocal factory states and declarative mapping bases. Add a get_db() context helper.
  - Create `backend/models.py` defining full structural schema tables mapping database structures:
    * User (id, name, email, hashed_password, exam_target, exam_date, created_at, is_active)
    * MoodEntry (id, user_id, mood_score, emotion_tags, note, energy_level, sleep_hours, study_hours, logged_at)
    * AssessmentResult (id, user_id, phq_score, gad_score, pss_score, overall_level, answers_json, taken_at)
    * ActivityLog (id, user_id, activity_type, duration_minutes, description, logged_at)
    * ChatMessage (id, user_id, role, content, sent_at)
    * AllyConnection (id, student_id, ally_name, ally_email, role, is_verified, created_at)
    * AllyNudge (id, connection_id, generated_at, insight_summary, actionable_tip, is_viewed)
  - Interlink relationship mapping layers across models (`User.moods`, `User.allies`, `AllyConnection.nudges`).
  - Create a migration initialize script at `backend/init_db.py` reading:
    from backend.database import engine, Base
    from backend.models import User
    Base.metadata.create_all(bind=engine)
    print("DB_INITIALIZED")
VALIDATION: Execute `python backend/init_db.py` and verify it terminates cleanly while creating file route `data/saathi.db`.
STATUS: TODO


=== PHASE 2: FASTAPI APPARATUS SETUP & AUTH CIRCUITS ===

TASK-005: Core Gateway Inception and Route Tree Assembly
DESCRIPTION: Construct the primary operational framework router endpoints setup attaching middleware and health pipelines.
STEPS:
  - Create the system core file `backend/main.py` instantiating `FastAPI(title="Saathi API")`.
  - Append open-access system settings hooks using `CORSMiddleware`.
  - Include structural path placeholders inside separate functional module files under `backend/routers/`: `auth_router.py`, `mood.py`, `assessment.py`, `ai_features.py`, `calendar.py`, `activity.py`, `analytics.py`, and `ally.py`. Ensure every module maps an instantiated `router = APIRouter()`.
  - Bind all structural modules to `app` using exact pattern prefix hooks inside `backend/main.py`.
  - Deploy a baseline pathway tracking route `@app.get("/health")` returning standard JSON status markers.
VALIDATION: Spin up background process hosting `uvicorn backend.main:app --port 8000` and confirm checking request to `http://localhost:8000/health` answers `{"status": "ok", "app": "Saathi"}`.
STATUS: TODO

TASK-006: Hashing Cryptography and Token Processing Systems
DESCRIPTION: Secure encryption layer parameters handling password transforms and JWT encoding/decoding sequences.
STEPS:
  - Create `backend/auth.py` initiating a passlib verification Context targeting standard bcrypt workflows.
  - Implement access code encoding actions configuring token life constraints using system parameters.
  - Setup an asynchronous dependency extraction engine named `get_current_user` checking verification context headers, translating sub credentials, and validating matches against SQLite table users.
VALIDATION: Run isolated test queries validating password matches and verify that bad or missing verification headers throw error code 401.
STATUS: TODO

TASK-007: Validation Request/Response Schemas Creation
DESCRIPTION: Construct Pydantic DTO interface structures managing data validation boundaries.
STEPS:
  - Create `backend/schemas.py`.
  - Add request configurations matching input variables: `UserCreate`, `LoginRequest`, `MoodCreate`, `AssessmentCreate`, `ActivityCreate`, and `AllyConnectionCreate`.
  - Add corresponding structural target payload footprints optimizing output views safely: `UserOut`, `Token`, `MoodOut`, `AssessmentOut`, `AllyConnectionOut`, and `AllyNudgeOut`. Set `from_attributes = True` on all data classes.
VALIDATION: Execute validation checks running test sequences passing input samples into `UserCreate` models to confirm type error detections operate normally.
STATUS: TODO

TASK-008: Authentication Endpoint Deployment
DESCRIPTION: Program user onboarding routes enabling data creation inputs and generating authorization keys.
STEPS:
  - Complete `backend/routers/auth_router.py` logic blocks providing endpoints `/register`, `/login`, and checking path `/me`.
  - Wire duplicate criteria validations to reject existing registration records trying to double-allocate matching email paths.
VALIDATION: Submit registration validation parameters through an HTTP POST network test client toward `/auth/register` and ensure it answers with a token object.
STATUS: TODO


=== PHASE 3: TELEMETRY PROCESSING LABS & DATA ARRAYS ===

TASK-009: Daily Mood and Emotion Logger Routing
DESCRIPTION: Code standard operational data routes logging structural metrics, emotion markers, and notes records.
STEPS:
  - Complete backend endpoints inside `backend/routers/mood.py`.
  - Wire route tracking hooks handler `POST /` saving incoming fields straight into database tables.
  - Formulate listing pipelines matching paths `GET /history` parsing filter window limitations via URL query parameters, alongside an evaluation route handler `GET /today`.
VALIDATION: Issue an authorized POST query toward `/mood/` mapping sample inputs and check that records land safely in structural data cells.
STATUS: TODO

TASK-010: Assessment Tracking Matrix Integration
DESCRIPTION: Provision non-clinical stress analysis questionnaire components returning diagnostic level markers.
STEPS:
  - Complete backend route blocks inside `backend/routers/assessment.py`.
  - Store the full 20-item tracking sequence within an extraction route mapping `GET /questions` (Items 1-9 PHQ, 10-16 GAD, 17-20 PSS).
  - Implement structural mapping score scripts at `POST /` converting multi-choice parameters into composite scores, determining operational stress levels (mild, moderate, severe), and logging values inside schema tables.
VALIDATION: Send an authorized array profile containing exactly 20 choice metrics inside a JSON packet to the assessment endpoint, and assert execution parameters process evaluation states cleanly.
STATUS: TODO

TASK-011: Static Asset Calendars Setup
DESCRIPTION: Establish timeline parsing mechanics logging tracking specifications for standard testing frameworks.
STEPS:
  - Populate explicit chronological json markers inside `data/exams.json` covering key testing platforms (NEET, JEE, CUET, CAT, GATE, UPSC, Boards). Ensure links, registration boundaries, and check windows exist.
  - Complete routes inside `backend/routers/calendar.py` configuring filter lookups under `GET /exams` and time alerts under `GET /upcoming`.
VALIDATION: Dispatch query calls checking target route path `/calendar/upcoming?days=120` and evaluate chronological layout alignments.
STATUS: TODO

TASK-012: Activity Restorer Tracking Routes
DESCRIPTION: Construct performance monitoring hooks noting tracking variables, active breaks, and social choices.
STEPS:
  - Complete script segments inside `backend/routers/activity.py` configuring system tool advice strings for break types.
  - Program capture pipelines via `POST /log` recording duration boundaries and descriptive identifiers.
  - Map calculation trackers via `GET /today` returning aggregate performance metrics for the day.
VALIDATION: Send structured transaction requests detailing an exercise completion event and verify data tracking metrics calculate correctly.
STATUS: TODO


=== PHASE 4: AI CHANNELS & CO-PILOT ADULT NUDGE SYSTEM ===

TASK-013: Generative AI Orchestration Service Layer
DESCRIPTION: Construct programmatic abstraction wrappers managing contextual text synthesis calls using Anthropic systems.
STEPS:
  - Complete `backend/services/ai_service.py` referencing standard operational system identities matching target client setups.
  - Build narrative creator functions (`generate_story`) passing student milestones into multi-part character logs.
  - Build support conversation logic workflows (`chat_with_student`) retaining running context states and embedding critical safety numbers.
  - Implement privacy-first data masking tool `generate_subtle_ally_nudge` reading student behavioral drops to output instructional care cards for parents/teachers without exposing underlying numeric logs.
VALIDATION: Run baseline script evaluation executions ensuring synthesis functions return clean text components bounded accurately within size constraints.
STATUS: TODO

TASK-014: AI Capabilities Routing Layouts
DESCRIPTION: Expose functional synthesis pipelines through standard operational endpoints.
STEPS:
  - Complete routing code configurations inside `backend/routers/ai_features.py` exposing access links toward text synthesis resources (`/story`, `/tip`, `/chat`, `/insight`).
  - Add query logic checking existing mood context profiles before triggering external generation calls.
VALIDATION: Execute a text request call targeting route `/ai/tip` and verify it handles output allocations cleanly.
STATUS: TODO

TASK-015: Subtle Ally Action Items Processor
DESCRIPTION: Construct proxy authorization tools allowing students to connect adult guides safely without data exposure risks.
STEPS:
  - Complete routing mechanics inside `backend/routers/ally.py` managing permission updates under path `POST /invite`.
  - Design calculation automation controllers generating parent/teacher care cards based on user metrics trends.
  - Expose specialized access paths matching `GET /nudges` allowing linked parental profiles to safely pull text advice cards.
VALIDATION: Fire invitation metrics payload streams and confirm generation routines translate high tension indicators into non-alarmist care directions.
STATUS: TODO

TASK-016: Analytical Evaluation Matrices and Escalation Lifelines
DESCRIPTION: Implement data trends calculations tracking moving metric metrics patterns and displaying emergency support hotlines.
STEPS:
  - Complete background calculation models inside `backend/services/analytics_service.py` checking consecutive performance indices over trailing assessment timelines.
  - Complete endpoints under `backend/routers/analytics.py` matching `/summary` and path `/escalation-check`.
  - Inject automatic risk state overrides turning safety flag evaluations to true if extreme metrics parameters trigger.
VALIDATION: Forge artificial database rows representing low performance logs and confirm route `/analytics/escalation-check` changes state instantly.
STATUS: TODO


=== PHASE 5: STREAMLIT FRONT-END INTERFACE ASSEMBLY ===

TASK-017: Network Client Engine and Session State Hooks
DESCRIPTION: Program communication bridges connecting interface assets straight to backend servers.
STEPS:
  - Complete `frontend/utils/api_client.py` setting up an unified connection library managing headers and timeouts.
  - Complete state helper definitions inside `frontend/utils/session.py` handling security tokens across code re-runs.
VALIDATION: Load validation modules verifying client connections can route queries across server lines cleanly.
STATUS: DONE

TASK-018: App Framework Workspace Layout and Authorization Gate
DESCRIPTION: Build the primary user workspace framing structural presentation controls and side navigation elements.
STEPS:
  - Complete core initialization sequences inside `frontend/app.py` setting page parameters and navigation routes.
  - Implement login check logic blocks blocking application features until secure validation configurations verify.
  - Integrate visual message alerts streaming daily motivation tips inside primary container areas.
VALIDATION: Launch interface using `streamlit run frontend/app.py` and confirm login selection menus render properly.
STATUS: DONE

TASK-019: Main Student Status Dashboard Screen
DESCRIPTION: Create primary analytics interface windows formatting performance metric counters and time metrics logs.
STEPS:
  - Complete `frontend/pages/1_Dashboard.py`.
  - Map chart setups consuming history list arrays and converting records into clean tracking graphs.
  - Add emergency alert blocks displaying critical hotline channels if backend evaluations report extreme stress states.
VALIDATION: Load dashboard view screens using test accounts and check that graphical plots track cleanly.
STATUS: DONE

TASK-020: Participant Check-In Logging Window
DESCRIPTION: Design data input form sliders logging physical habits and emotional context indices.
STEPS:
  - Complete `frontend/pages/2_Mood_Check_In.py`.
  - Build selection interfaces mapping numeric values alongside custom tag configurations tracking current stress vectors.
  - Connect database save pathways triggering transaction transmissions upon activation clicks.
VALIDATION: Complete data fields on check-in tracking pages, submit entries, and check that backend servers record data appropriately.
STATUS: DONE

TASK-021: Evaluation Survey Questionnaire Panel
DESCRIPTION: Program the interactive structural assessment screen handling multi-choice diagnostic arrays.
STEPS:
  - Complete `frontend/pages/3_Assessment.py` iterating questions through separate loop index steps.
  - Inject safety text indicators preceding sensitive checklist items to protect participant tracking comfort.
  - Lock submission processing routines unless every diagnostic element registers choice metrics.
VALIDATION: Step through survey sections, hit verification triggers, and ensure results cards populate cleanly.
STATUS: DONE

TASK-022: Relatable Narrative Mirror Screen
DESCRIPTION: Assemble projective visualization screens displaying generated scenario blocks.
STEPS:
  - Complete `frontend/pages/4_AI_Story.py` connecting text processing tools to generation buttons.
  - Build feedback validation options logging situational matching indices and rendering matching comfort text arrays.
VALIDATION: Trigger sample story sequences on-screen and verify transition flows change UI maps predictably.
STATUS: DONE

TASK-023: Testing Timelines and Conversational Support Screens
DESCRIPTION: Code scheduling information views alongside empathetic artificial helper chat interfaces.
STEPS:
  - Complete `frontend/pages/5_Exam_Calendar.py` formatting schedule information variables into legible grids.
  - Complete `frontend/pages/6_AI_Chat.py` constructing message display containers with memory buffer limits.
VALIDATION: Open conversation interfaces, verify message logs render correctly, and test calendar display filters.
STATUS: DONE

TASK-024: Recovery Operations and Guarded Co-Pilot View Screens
DESCRIPTION: Implement restoration helper tools and private adult communication management options.
STEPS:
  - Complete `frontend/pages/7_Activity_Break.py` tracking timer sequences alongside active rest logs.
  - Complete `frontend/pages/8_Subtle_Ally.py` enabling users to invite adult guides, check activation status metrics, and view masked outbox instruction card previews.
  - Complete `frontend/pages/9_Resources.py` cataloging help groups, system links, and administrative form checklists.
VALIDATION: Verify ally view menus mask underlying metrics, showing only the translated, actionable tips.
STATUS: DONE


=== PHASE 6: QUALITY CONTROL & AUTOMATED VALIDATION ===

TASK-025: End-to-End Core Automation Suite Execution
DESCRIPTION: Launch programmatic diagnostic test cases verifying API endpoints process instructions securely according to schema parameters.
STEPS:
  - Create integration verification scripts at `backend/test_suite.py` executing programmatic user setups, data logging tests, privacy masking loops, and metric safety checks.
  - Ensure all database state interactions use explicit test entries that clear gracefully post-evaluation.
VALIDATION: Run terminal instruction `python backend/test_suite.py` and confirm all internal validation test profiles succeed without exit warnings.
STATUS: TODO