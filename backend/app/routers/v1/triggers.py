from models.comment import Comment
from models.task import Task
from fastapi import APIRouter, HTTPException, status
from models.todo import Todo, TodoEvent, TodoIn, TodoId, TodoUpdate, TodoOut
from models.column import Column
from models.progress_indicator import ProgressStatus
from bson.objectid import ObjectId
from datetime import datetime
import pusher
from database import TodoCollection, TaskCollection, TodoTimerCollection, ProgressIndicatorCollection, TodoColumnCollection
from repositories.todo_repository import TodoRepository
from repositories.column_repository import ColumnRepository
from repositories.progress_indicator_repository import ProgressIndicatorRepository

router = APIRouter()

todo_repository = TodoRepository()
todo_column_repository = ColumnRepository()
progress_indicator_repository = ProgressIndicatorRepository()


def reset_todos():
    todos = todo_repository.find_todos_by_status('today')
    todo_ids = [str(todo['_id']) for todo in todos]
    todo_repository.update_many_status('today', 'todo')
    
    todo_column = Column(**todo_column_repository.find_by_name('todo'))
    column_todos = list(set(todo_column.todos + todo_ids))
    todo_column_repository.update_todos_by_name('todo', column_todos) # Refactor later to one update
    todo_column_repository.update_todos_by_name('today', [])

def check_progress():
    todos_in_progress_count = todo_repository.count_by_status('today')
    todos_completed_today_count = todo_repository.count_completed_today()
    total_today_tasks = todos_completed_today_count + todos_in_progress_count

    if total_today_tasks == 0:
        progress_indicator_repository.update_status('good')
        return 'good'

    percentage_complete = todos_completed_today_count / total_today_tasks
    if percentage_complete <= 0.25:
        return ProgressStatus.WORSE.value
    elif percentage_complete <= 0.5:
        return ProgressStatus.BAD.value
    elif percentage_complete <= 0.75:
        return ProgressStatus.MODERATE.value
    else:
        return ProgressStatus.GOOD.value
    
def trigger_pusher(progress_status):
    pusher_client = pusher.Pusher(app_id=u'1309679', key=u'1700ce6fce54e4eb675f', secret=u'8341de910460183be951', cluster=u'eu')
    pusher_client.trigger(u'todos', u'event', {u'progress_status': progress_status})


@router.post("/")
def trigger_scheduler(event: TodoEvent):
    try:
        if event.type == 'reset':
            reset_todos()
        elif event.type == 'check_progress':
            progress_status = check_progress()
            progress_indicator_repository.update_status(progress_status)
            trigger_pusher(progress_status)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event of type {event.type} does not exist")
        
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    # try:
    #     if event.type == 'reset':
    #         # rest all the in progress tasks to todo.
    #         todoIds = [ todo['_id'] for todo in TodoCollection.find({'status': 'today'})]
    #         result = TodoCollection.update_many({'status': 'today'},{ 
    #             "$set": { "status" : "todo" } 
    #         })
            
    #         column = Column(**TodoColumnCollection.find_one({'name': 'todo'}))
    #         column_todos = list(set(column.todos + todoIds))
    #         # TODO check that update has taken place
    #         todo_column_results = TodoColumnCollection.update_one({'name': 'todo'}, {'$set': {'todos': column_todos}})
    #         today_column_results = TodoColumnCollection.update_one({'name': 'today'}, {'$set': {'todos': []}})
    #     elif event.type == 'check_progress':
    #         # check if number of tickets close are greater than the tickets open or at 30% or 50 % of tickets opened and change face.
    #         start_time =  datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    #         todos_in_progress_count =  TodoCollection.count_documents({'status': 'today'})
    #         todos_completed_today_count = TodoCollection.count_documents({'status': 'done', 'modified_at': {'$gte': start_time}})
    #         print(f"Midnight date = {start_time}, number of tasks in progress = {todos_in_progress_count}, number of tickets closed today {todos_completed_today_count}")
    #         total_today_tasks = todos_completed_today_count+todos_in_progress_count
    #         print(total_today_tasks)
    #         if total_today_tasks == 0:
    #             print("In here and return")
    #             progress_indicator = ProgressIndicatorCollection.find_one_and_update({}, {'$set': {"progress_status": 'good'}})
    #             print(progress_indicator)
    #             pusher_client = pusher.Pusher(app_id=u'1309679', key=u'1700ce6fce54e4eb675f', secret=u'8341de910460183be951', cluster=u'eu')
    #             pusher_client.trigger(u'todos', u'event', {u'progress_status': u'good'})
    #             return {"status": "success"}
            
    #         percentage_complete = todos_completed_today_count/(todos_completed_today_count+todos_in_progress_count)
    #         progress_status = None
    #         if percentage_complete <= 0.25:
    #             progress_status = ProgressStatus.WORSE
    #         elif percentage_complete > 0.25 and percentage_complete <= 0.5:
    #             progress_status = ProgressStatus.BAD
    #         elif percentage_complete > 0.5 and percentage_complete <= 0.75:
    #             progress_status = ProgressStatus.MODERATE
    #         elif percentage_complete > 0.75 and percentage_complete <= 1:
    #             progress_status = ProgressStatus.GOOD
    #         else:
    #             raise Exception(f"Incorrect progress percentage {percentage_complete}")
            
    #         # TODO update collection with the correct value
    #         progress_indicator = ProgressIndicatorCollection.find_one_and_update({}, {'$set': {"progress_status": progress_status.value}})
    #         print(progress_indicator)
    #         pusher_client = pusher.Pusher(app_id=u'1309679', key=u'1700ce6fce54e4eb675f', secret=u'8341de910460183be951', cluster=u'eu')
    #         pusher_client.trigger(u'todos', u'event', {u'progress_status': progress_status.value})
    #     else:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event of type {event.type} does not exit")
        
    #     return {"status": "success"}
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))