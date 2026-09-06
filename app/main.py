from fastapi import FastAPI

from app.routers import todos

app = FastAPI(
    title="To-Do API",
    description="API REST de to-do com PostgreSQL e Alembic",
    version="1.0.0",
)

app.include_router(todos.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
