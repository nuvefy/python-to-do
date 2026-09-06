import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import todo as todo_crud
from app.database import get_db
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)) -> TodoResponse:
    return todo_crud.create_todo(db, todo_in)


@router.get("", response_model=list[TodoResponse])
def list_todos(
    completed: bool | None = Query(None),
    db: Session = Depends(get_db),
) -> list[TodoResponse]:
    return todo_crud.list_todos(db, completed=completed)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: uuid.UUID, db: Session = Depends(get_db)) -> TodoResponse:
    todo = todo_crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: uuid.UUID,
    todo_in: TodoUpdate,
    db: Session = Depends(get_db),
) -> TodoResponse:
    todo = todo_crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo_crud.update_todo(db, todo, todo_in)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    todo = todo_crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todo_crud.delete_todo(db, todo)
