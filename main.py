from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.health import router as health_router
from app.routes.chat import router as chat_router
from app.routes.reset import router as reset_router


app = FastAPI(
    title="Trendly Agentic Support Assistant"
)

# API Routes
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(reset_router)

# Frontend
app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)