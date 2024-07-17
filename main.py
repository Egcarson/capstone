from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Hello, Visitor! You've reached the capstone project.....Navigate to /docs to view the magic :)"}
