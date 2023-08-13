from models.task import Task
from fastapi import APIRouter, status
from repositories.task_repository import TaskRepository


router = APIRouter()

task_repository = TaskRepository()

@router.get("/", response_model=list[Task])
def get_tasks(todo_id: str):
    # tasks = []
    # for task in TaskCollection.find({"todo_id": ObjectId(todo_id)}):
    #     tasks.append(Task(**task))
    # return tasks
    return task_repository.find_by_todo_id(todo_id=todo_id)


@router.get("/{task_id}", response_model=Task)
def get_task(todo_id: str, task_id: str):
    # data = TaskCollection.find_one({'_id': ObjectId(task_id)})
    # return Task(**data)
    return task_repository.find_by_id(id=task_id)

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: str):
    # TaskCollection.delete_one({'_id': ObjectId(task_id)})
    task_repository.delete(id=task_id)