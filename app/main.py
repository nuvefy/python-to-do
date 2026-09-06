from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routers import todos, ui

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title="To-Do API",
    description="API REST de to-do com PostgreSQL e Alembic",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(todos.router)
app.include_router(ui.router)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/ui")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
