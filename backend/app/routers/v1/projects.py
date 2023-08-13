from fastapi import APIRouter
from models.project import Project, ProjectId, ProjectIn
from bson.objectid import ObjectId
from database import ProjectCollection
from repositories.project_repository import ProjectRepository

router = APIRouter()
project_repository = ProjectRepository()
from typing import List

@router.get("/", response_model=List[Project])
def get_projects():
    # projects = []
    # for project in project_repository.find_all():
    #     projects.append(Project(**project))
    return project_repository.find_all()


@router.get("/{project_id}", response_model=Project)
def get_project_by_id(project_id: str):
    # data = ProjectCollection.find_one({'_id': ObjectId(project_id)})
    return project_repository.find_by_id(id=project_id)

@router.post("/", response_model=ProjectId)
def create_project(project: ProjectIn):
    project_dict = project.dict()
    # data = ProjectCollection.insert_one(project_dict).inserted_id
    id = project_repository.insert_one(project_dict)
    return ProjectId(id=id)


# @router.patch("/{id}")
# def update_todo(id: str, todo_update: TodoUpdate):
#     # update = todo.dict()
#     # print(update)
#     # del update['id']
#     # try:
#     data = db.todos.update_one({'_id': ObjectId(id)}, {'$set': {'description': todo_update.description}})
#     # add tasks to task table
#     new_tasks = [Task(title=task, status=False, todo_id=ObjectId(id)).dict() for task in todo_update.new_tasks]
#     updated_tasks =[Task(**task) for task in todo_update.updated_tasks]
#     if len(new_tasks) > 0: db.tasks.insert_many(new_tasks)
#     if len(updated_tasks) > 0:
#         for task in updated_tasks:
#             # print(task)
#             db.tasks.find_one_and_update({'_id': task.id}, {'$set': {'status': task.status}})
#     return {"status": "success"}
#     # except:
#     #     raise HTTPException(status_code=500, detail="Failed to update todo")