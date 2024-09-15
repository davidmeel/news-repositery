import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from starlette import status
from sqlalchemy.orm import Session
import aiofiles

from models.post import PostFiles, Post
from models.users import UserTable
from database import get_session
from dependencies.users.user import user_handler
from directories.post import create_dir as post_create_dir
from config import MEDIA_ROOT
from descriptions.files import *

router = APIRouter(
    prefix="/files",
    tags=['files']
)
from fastapi import HTTPException

# Create a file
@router.post("/", status_code=status.HTTP_201_CREATED, description=create_file_description)
async def create_file(
    file: UploadFile = File(...), post_id: int = Form(...),
    user: UserTable = Depends(user_handler.employee), 
    session: Session = Depends(get_session)
):
    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    post = session.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    # Generate the file path before inserting the record
    file_data = await post_create_dir(post_id=post_id, filename=file.filename)
    file_full_path = file_data['file_full_path']
    file_dir_for_django = file_data['file_dir'] + file.filename

    # Save the file to the filesystem
    content = await file.read()
    async with aiofiles.open(file_full_path, 'wb') as out_file:
        await out_file.write(content)

    post_files = PostFiles(
        post_id=post_id,
        file=file_dir_for_django
    )
    
    session.add(post_files)
    session.commit()
    session.refresh(post_files)

    return {"message": "Post File Created!"}




# Update a file
@router.put("/{file_id}", status_code=status.HTTP_200_OK, description=update_file_description)
async def update_file(
    file_id: int,
    file: UploadFile = File(...),
    user: UserTable = Depends(user_handler.employee), 
    session: Session = Depends(get_session)
):
    post_files = session.query(PostFiles).filter(PostFiles.id == file_id).first()
    if not post_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # Delete old file
    old_file_path = f"{MEDIA_ROOT}{post_files.file}"
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    # Save new file
    file_data = await post_create_dir(post_id=post_files.post_id, filename=file.filename)
    content = await file.read()
    async with aiofiles.open(file_data['file_full_path'], 'wb') as out_file:
        file_dir_for_django = file_data['file_dir'] + file.filename
        await out_file.write(content)

    post_files.file = file_dir_for_django
    session.commit()
    session.refresh(post_files)

    return {"message": "Post File Updated!"}



# Delete a file
@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT, description=delete_file_description)
async def delete_file(file_id: int, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):

    post_files = session.query(PostFiles).filter(PostFiles.id == file_id).first()
    if not post_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # Delete file from the filesystem
    file_path = f"{MEDIA_ROOT}{post_files.file}"
    if os.path.exists(file_path):
        os.remove(file_path)

    session.delete(post_files)
    session.commit()

