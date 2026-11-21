from fastapi import FastAPI
from routers.health import healthRouter

app = FastAPI(title="Taskbox-api")

app.include_router(healthRouter)
