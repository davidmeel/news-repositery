from fastapi import FastAPI
from routers import auth, post, comments, favorites, files


app = FastAPI(title="NEWS API")


app.include_router(router=auth.router)
app.include_router(router=post.router)
app.include_router(router=comments.router)
app.include_router(router=favorites.router)
app.include_router(router=files.router)





