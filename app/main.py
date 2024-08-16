from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth, movies, ratings, comment
import app.models as models
from app.database import engine
from app.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# create database tables based on defined models
# you can remove this if you are pulling with alembic
models.Base.metadata.create_all(bind=engine)

origins = ["*"]  # Sir this is for development purposes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)
app.include_router(comment.router)


@app.get('/')
async def root():
    logger.info("API accessed.")
    return {"message": "Hello world!! Welcome to my capstone project"}
