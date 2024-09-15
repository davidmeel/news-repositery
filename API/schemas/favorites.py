from pydantic import BaseModel, Field
from typing import List, Optional



class FavoritesResponseSchema(BaseModel):
    user_id: int
    post_id: int

    class Config:
        from_attributes=True


# class FavoriteCreateSchema(BaseModel):
#     post_id: int