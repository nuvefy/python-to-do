import uuid
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import todo as todo_crud
from app.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(prefix="/ui", tags=["ui"])


def _parse_due_date(value: str | None) -> date | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return date.fromisoformat(value)


def _get_todo_or_404(db: Session, todo_id: uuid.UUID) -> Todo:
    todo = todo_crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.get("", response_class=HTMLResponse)
def ui_index(
    request: Request,
    completed: bool | None = Query(None),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    todos = todo_crud.list_todos(db, completed=completed)
    return templates.TemplateResponse(
        request,
        "todos/index.html",
        {"todos": todos, "filter": completed},
    )


@router.post("/todos", response_class=HTMLResponse, response_model=None)
def ui_create_todo(
    request: Request,
    title: str = Form(...),
    description: str | None = Form(None),
    due_date: str | None = Form(None),
    db: Session = Depends(get_db),
) -> HTMLResponse | RedirectResponse:
    description = description.strip() if description else None
    if description == "":
        description = None
    todo = todo_crud.create_todo(
        db,
        TodoCreate(
            title=title.strip(),
            description=description,
            due_date=_parse_due_date(due_date),
        ),
    )
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request,
            "todos/_item.html",
            {"todo": todo},
        )
    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/todos/{todo_id}", response_class=HTMLResponse)
def ui_get_todo(
    request: Request,
    todo_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    todo = _get_todo_or_404(db, todo_id)
    return templates.TemplateResponse(
        request,
        "todos/_item.html",
        {"todo": todo},
    )


@router.get("/todos/{todo_id}/edit", response_class=HTMLResponse)
def ui_edit_todo(
    request: Request,
    todo_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    todo = _get_todo_or_404(db, todo_id)
    return templates.TemplateResponse(
        request,
        "todos/_edit.html",
        {"todo": todo},
    )


@router.post("/todos/{todo_id}", response_class=HTMLResponse, response_model=None)
def ui_update_todo(
    request: Request,
    todo_id: uuid.UUID,
    title: str = Form(...),
    description: str | None = Form(None),
    due_date: str | None = Form(None),
    completed: str | None = Form(None),
    db: Session = Depends(get_db),
) -> HTMLResponse | RedirectResponse:
    todo = _get_todo_or_404(db, todo_id)
    description = description.strip() if description else None
    if description == "":
        description = None
    todo = todo_crud.update_todo(
        db,
        todo,
        TodoUpdate(
            title=title.strip(),
            description=description,
            due_date=_parse_due_date(due_date),
            completed=completed == "true",
        ),
    )
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request,
            "todos/_item.html",
            {"todo": todo},
        )
    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/todos/{todo_id}/toggle", response_class=HTMLResponse, response_model=None)
def ui_toggle_todo(
    request: Request,
    todo_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> HTMLResponse | RedirectResponse:
    todo = _get_todo_or_404(db, todo_id)
    todo = todo_crud.update_todo(
        db,
        todo,
        TodoUpdate(completed=not todo.completed),
    )
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request,
            "todos/_item.html",
            {"todo": todo},
        )
    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/todos/{todo_id}/delete", response_class=HTMLResponse, response_model=None)
def ui_delete_todo(
    request: Request,
    todo_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Response:
    todo = _get_todo_or_404(db, todo_id)
    todo_crud.delete_todo(db, todo)
    if request.headers.get("HX-Request"):
        return Response(content="", status_code=status.HTTP_200_OK)
    return RedirectResponse(url="/ui", status_code=status.HTTP_303_SEE_OTHER)
