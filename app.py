from fastapi import FastAPI
from routers import poll_router

app = FastAPI()

app.include_router(poll_router.router)
