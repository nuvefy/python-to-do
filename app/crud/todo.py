import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


def create_todo(db: Session, todo_in: TodoCreate) -> Todo:
    todo = Todo(
        title=todo_in.title,
        description=todo_in.description,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todo(db: Session, todo_id: uuid.UUID) -> Todo | None:
    return db.get(Todo, todo_id)


def list_todos(db: Session, completed: bool | None = None) -> list[Todo]:
    stmt = select(Todo).order_by(Todo.created_at.desc())
    if completed is not None:
        stmt = stmt.where(Todo.completed.is_(completed))
    return list(db.scalars(stmt).all())


def update_todo(db: Session, todo: Todo, todo_in: TodoUpdate) -> Todo:
    data = todo_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(todo, field, value)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: Todo) -> None:
    db.delete(todo)
    db.commit()
