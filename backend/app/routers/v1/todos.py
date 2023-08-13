from models.comment import Comment
from models.task import Task
from fastapi import APIRouter, HTTPException, status
from models.todo import Todo, TodoIn, TodoId, TodoUpdate, TodoOut
from bson.objectid import ObjectId
from database import TodoTimerCollection
from repositories.todo_repository import TodoRepository
from repositories.task_repository import TaskRepository
from repositories.comment_repository import CommentRepository

router = APIRouter()
todo_repository = TodoRepository()
task_repository = TaskRepository()
comment_repository = CommentRepository()

@router.get("/", response_model=list[TodoOut])
def get_todos():
    todos = []
    try:
        for todo_db in todo_repository.find_all():
            todo: TodoOut = TodoOut(**todo_db)
            todo.num_tasks = task_repository.count_by_todo_id(todo.id)
            todo.num_completed_tasks = task_repository.count_completed_by_todo_id(todo.id)
            todos.append(todo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return todos

@router.get("/by_project/{project_id}")
def get_todos_by_project_Id(project_id: str):
    todos = [TodoOut(**todo) for todo in todo_repository.find_by_project_id(project_id)]
    
    for todo in todos:
        accumulated_time = 0
        timers = TodoTimerCollection.find({"todo_id": ObjectId(todo.id)})
        for timer in timers:
            accumulated_time +=timer.accumulated_time
    return todos


@router.get("/{item_id}")
def get_todo_by_id(item_id: str):
    data = todo_repository.find_by_id(item_id)
    if not data:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(**data)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoIn):
    todo.create_timestamp()
    todo_dict = todo.dict()
    todo_id = todo_repository.create(todo_dict)
    return TodoId(id=todo_id)


@router.patch("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(id: str, todo_update: TodoUpdate):
    try:
        todo_update.update_timestamp()
        todo_update_dict = {k: v for k, v in todo_update.dict().items() if v is not None and k not in ['new_tasks', 'updated_tasks', 'new_comments', 'updated_comments']}
        todo_repository.update(id, todo_update_dict)
        
        # Handle tasks and comments updates
        if todo_update.new_tasks:
            task_repository.create_many([Task(**task, todo_id=id) for task in todo_update.new_tasks])
        if todo_update.updated_tasks:
            print(todo_update.updated_tasks)
            task_repository.update_many([Task(**task) for task in todo_update.updated_tasks])
        if todo_update.new_comments:
            comment_repository.create_many([Comment(text=comment, todo_id=id) for comment in todo_update.new_comments])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update todo: {str(e)}")

@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_id: str):
    if not todo_repository.delete(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")