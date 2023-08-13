import os
from pymongo import MongoClient


client = MongoClient(os.environ['MONGODB_URL'])


db = client['today']

TodoCollection = db.todos
TaskCollection = db.tasks
CommentCollection = db.comments
TodoTimerCollection = db.todotimers
ProjectCollection = db.projects
TodoColumnCollection = db.todocolumns
ProgressIndicatorCollection = db.progressindicator


columns = [{
    "col_ref": "column_1",
    "name": "todo",
    "color": "red",
    "todos": []
    },
    {
    "col_ref": "column_2",
    "name": "today",
    "color": "yellow",
    "todos": []
    },
    {
    "col_ref": "column_3",
    "name": "done",
    "color": "green",
    "todos": []
   }
]

if TodoColumnCollection.count_documents({}) != len(columns):
    TodoColumnCollection.drop()
    TodoColumnCollection.insert_many(columns)
    
if ProgressIndicatorCollection.count_documents({}) == 0:
    initial_progress = {"progress_status": "good"}
    ProgressIndicatorCollection.insert_one(initial_progress)