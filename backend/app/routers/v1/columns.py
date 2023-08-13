from models.column import Column
from fastapi import APIRouter, HTTPException, status

from repositories.column_repository import ColumnRepository

column_repository = ColumnRepository()

router = APIRouter()

@router.get("/", response_model=list[Column])
def get_columns():
    return column_repository.find_all()

@router.patch("/{id}", response_model=Column)
def update_column(id: str, todos: list):
     # Update the column
    result = column_repository.update_todos(id, todos)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
    
    # Fetch the updated column
    updated_column = column_repository.find_by_id(id)
    
    if not updated_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Updated column not found")
    
    # Return the updated column
    return Column(**updated_column)