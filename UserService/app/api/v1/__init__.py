from fastapi import APIRouter

from UserService.app.api.v1.user import router as user_router

router = APIRouter(prefix='/api/v1')

router.include_router(user_router)
