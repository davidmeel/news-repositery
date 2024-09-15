from pydantic import BaseModel, Field
from typing import List, Optional




class CommentResponseSchema(BaseModel):
    user_id: int
    text: str

    # class Config:
    #     from_attributes=True


class CommentCreateSchema(BaseModel):
    post_id: int
    text: str = Field(max_length=48)