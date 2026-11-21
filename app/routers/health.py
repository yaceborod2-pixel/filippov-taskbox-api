from fastapi import APIRouter

healthRouter = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@healthRouter.get("/")
def get_health():
    return {
        "status": "ok"
    }
