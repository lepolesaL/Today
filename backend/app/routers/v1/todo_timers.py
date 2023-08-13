from models.todo_timer import TodoTimer ,TodoTimerId, TodoTimerUpdate
from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId

from repositories.todo_timer_repository import TodoTimerRepository

router = APIRouter()

todo_time_repository = TodoTimerRepository()


@router.post("/")
def create_timer(todo_id: str, todoTimerIn: TodoTimer):
    todoTimer: TodoTimer = todoTimerIn.create(ObjectId(todo_id))
    id = todo_time_repository.insert_one(todoTimer.dict())
    return TodoTimerId(id=id)

@router.get("/", response_model=TodoTimer)
def get_timer(todo_id: str):
    # result = TodoTimerCollection.find_one({"todo_id": ObjectId(todo_id)}, sort=[("position", DESCENDING)])
    result = todo_time_repository.find_one_by_todo_id(todo_id=todo_id)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return result


@router.patch("/{id}")
def update_todo_timer(todo_id: str, id: str, todo_timer_update: TodoTimerUpdate):
    print(todo_timer_update)
    todo_timer_update.update_timestamp()
    print(todo_timer_update)
    try:
        # data = TodoTimerCollection.update_one({'_id': ObjectId(id), 'todo_id': ObjectId(todo_id)}, {'$set': {'status': todo_timer_update.status, 'accumulated_time': todo_timer_update.accumulated_time}})
        data = todo_time_repository.update_todo_timer(id=id, todo_id=todo_id, status=todo_timer_update.status, accumulated_time=todo_timer_update.accumulated_time)
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise  HTTPException(status_code=500, detail="Failed to update todo timer")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_timer(todo_id: str, id: str):
#    result = TodoTimerCollection.delete_one({'_id': ObjectId(id), 'todo_id': ObjectId(todo_id)})
    # result = todo_time_repository.delete(id=id)
    if not todo_time_repository.delete(id=id):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delete failed, item does not exist")