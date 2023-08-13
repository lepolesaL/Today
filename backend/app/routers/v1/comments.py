from typing import List
from models.comment import Comment
from fastapi import APIRouter, status

from repositories.comment_repository import CommentRepository
router = APIRouter()

comment_repository = CommentRepository()

@router.get("/", response_model=List[Comment])
def get_comments(todo_id: str):
    # comments = []
    # for comment in CommentCollection.find({"todo_id": ObjectId(todo_id)}):
    #     comments.append(Comment(**comment))
    return comment_repository.find_by_todo_id(todo_id=todo_id)


@router.get("/{comment_id}", response_model=Comment)
def get_comment(todo_id: str, comment_id: str):
    # data = CommentCollection.find_one({'_id': ObjectId(comment_id)})
    return comment_repository.find_by_id(id=comment_id)

@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id: str):
    # CommentCollection.delete_one({'_id': ObjectId(comment_id)})
    comment_repository.delete(id=comment_id)