from fastapi import APIRouter
from user.routers import router as user_router

router = APIRouter(prefix="/v1")

router.include_router(user_router, tags=["Users"])

