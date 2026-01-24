from fastapi import APIRouter, Depends, Path, Query, HTTPException
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from models import Todos
from database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field

router = APIRouter()

# Database session dependency - yields session and ensures cleanup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type alias for cleaner db dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

# Pydantic model for creating and fully updating todos (POST/PUT)
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: Optional[bool] = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example":{
                "title": "Go to the store",
                "description": "Pick up eggs",
                "complete": False,
                "priority": 5
            }
        }
    }

# Pydantic model for partial updates (PATCH) - all fields optional with None defaults
class TodoPartialUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = Field(default=None, min_length=3, max_length=100)
    priority: Optional[int] = Field(default=None, gt=0, lt=6)
    complete: Optional[bool] = None  # Must be None for exclude_unset to work properly

    model_config = {
        "json_schema_extra": {
            "example":{
                "title": "Go to the store",
                "description": "Pick up eggs",
                "complete": False,
                "priority": 5
            }
        }
    }

@router.get("/todo/", status_code=status.HTTP_200_OK)
async def read_all(
    db: db_dependency,
    title: Optional[str] = Query(default=None, min_length=3),
    complete: Optional[bool] = Query(default=None),
    priority: Optional[int] = Query(default=None, gt=0, lt=6)
):
    '''Read all Todos, optionally filter by title, complete, priority'''
    # Start with base query (lazy evaluation - no DB call yet)
    query = db.query(Todos)

    # Chain filters together - each adds to the query
    if title:
        query = query.filter(Todos.title == title)
    if complete is not None:  # Check 'is not None' to handle False values
        query = query.filter(Todos.complete == complete)
    if priority:
        query = query.filter(Todos.priority == priority)
    
    # Execute query with all filters combined
    return query.all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    '''Read todo by Id'''
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")

@router.post("/todo", status_code=status.HTTP_204_NO_CONTENT)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    '''Create a todo'''
    # Convert Pydantic model to SQLAlchemy model
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, 
                      todo_request: TodoRequest, 
                      todo_id: int = Path(gt=0)):
    '''Update todo by Id'''
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo Not Found.')

    # Update all fields from request
    update_data = todo_request.model_dump()
    for key, value in update_data.items():
        setattr(todo_model, key, value)

    db.commit()  # No db.add() needed - already tracked by session

@router.patch("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_partial(
    db: db_dependency,
    todo_request: TodoPartialUpdate,
    todo_id: int = Path(gt=0)
):
    '''Update todo partially'''
    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not Found.')
    
    # exclude_unset=True only includes fields explicitly provided in request
    update_data = todo_request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    
    db.commit()
    

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    '''Delete todo by Id'''
    # Direct delete without fetching (more efficient)
    deleted_count = db.query(Todos).filter(Todos.id==todo_id).delete()
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    db.commit()
