from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from models.post import PostFavorites
from models.post import Post
from models.users import UserTable
from database import get_session
from dependencies.users.user import user_handler
from descriptions.favorites import create_favorite_description, delete_favorite_description

router = APIRouter(
    prefix="/favorites",
    tags=['favorites']
)

@router.post("/", status_code=status.HTTP_201_CREATED, description=create_favorite_description)
def create_favorite(post_id: int, user: UserTable = Depends(user_handler.user), session: Session = Depends(get_session)):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    favorite = session.query(PostFavorites).filter(PostFavorites.post_id == post_id, PostFavorites.user_id == user.id).first()
    if favorite:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post is already in favorites.")

    new_favorite = PostFavorites(
        post_id=post_id,
        user_id=user.id
    )
    
    session.add(new_favorite)
    session.commit()
    session.refresh(new_favorite)
    return {"message": "Post added to favorites!"}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, description=delete_favorite_description)
def delete_favorite(post_id: int, user: UserTable = Depends(user_handler.user), session: Session = Depends(get_session)):
    favorite = session.query(PostFavorites).filter(PostFavorites.post_id == post_id, PostFavorites.user_id == user.id).first()

    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found!")

    session.delete(favorite)
    session.commit()
