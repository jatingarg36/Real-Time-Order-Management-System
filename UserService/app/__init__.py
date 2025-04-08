from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Startup Event Handler
    from UserService.app.core.config import startup
    await startup()

    # adding routers
    from UserService.app.api.v1 import router as v1_router
    app.include_router(v1_router)

    yield

    # On Shutdown Event Handler
    from UserService.app.core.config import shutdown
    await shutdown()


user_app = FastAPI(title='User Service',
                   docs_url='/user/api/docs',
                   description='Manages the user registration ',
                   lifespan=lifespan, middleware=[])

from UserService.app.middlewares.exceptions import ExceptionMiddleware
from UserService.app.middlewares.request_time_middleware import TimingMiddleware

user_app.add_middleware(ExceptionMiddleware)
user_app.add_middleware(TimingMiddleware)
