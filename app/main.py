from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import APP_NAME, APP_VERSION, STATIC_DIR
from app.api.health_routes import router as health_router
from app.api.role_routes import router as role_router
from app.api.diagnostic_routes import router as diagnostic_router
from app.api.learning_routes import router as learning_router
from app.api.knowledge_routes import router as knowledge_router
from app.api.control_routes import router as control_router
from app.api.case_routes import router as case_router
from app.api.report_routes import router as report_router

app = FastAPI(title=APP_NAME, version=APP_VERSION, description="AI-платформа для диагностики, обучения и сертификации специалистов по продажам")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(role_router)
app.include_router(diagnostic_router)
app.include_router(learning_router)
app.include_router(knowledge_router)
app.include_router(control_router)
app.include_router(case_router)
app.include_router(report_router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")
