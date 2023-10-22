from fastapi import FastAPI
from routes.user import user
from routes.post import post


app = FastAPI(
    title="Positive Blog"
)
app.include_router(user)
app.include_router(post)


@app.get("/")
async def hello() -> str:
    return "Hello World"

