from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models.post import Post
from sqlalchemy import select
from database import get_session
from models.users import UserTable
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from dependencies.users.user import user_handler
from descriptions.post import *
from schemas.post import (PostCreateSchema, PostListSchema, DetailSchema)

router = APIRouter(
    prefix="/news",
    tags=['news']
)


@router.get("/posts", response_model=list[PostListSchema], description=posts_description, status_code=status.HTTP_200_OK)
def get_posts(session: Session = Depends(get_session)):
    result = session.execute(
        select(Post)
        .options(joinedload(Post.files), joinedload(Post.category))
    )
    posts = result.unique().scalars().all()

    return [PostListSchema.from_orm(post) for post in posts]


@router.get("/posts/{post_id}", response_model=DetailSchema, description=post_detail_description, status_code=status.HTTP_200_OK)
async def get_post_detail(post_id: int, session: Session = Depends(get_session)):
    result = session.execute(
        select(Post).where(Post.id == post_id)
        .options(
            joinedload(Post.category),  
            joinedload(Post.user),
            joinedload(Post.files),
            joinedload(Post.comments),
            joinedload(Post.favorites)))
    post = result.unique().scalar_one_or_none()

    if not post: raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/posts", description=create_post_description, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreateSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    post = Post(
        title=data.title,
        description=data.description,
        category_id=data.category_id,
        user_id=user.id)
    try:
        session.add(post)
        session.commit()
        session.refresh(post)
        return {"message": "Post created!"}
    except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occurred")



@router.delete("/posts/{post_id}", description=delete_post_description, status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found !")
    session.delete(post)
    session.commit()
    