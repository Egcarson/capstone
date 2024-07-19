from fastapi import FastAPI
import routers.user
import routers.auth
import models
from database import engine

# create database tables based on defined models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(routers.auth.router)
app.include_router(routers.user.router)


@app.get('/')
async def root():
    return {"message": "Hello, Visitor! You've reached the capstone project.....Navigate to /docs to view the magic :)"}
