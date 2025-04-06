from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Startup Event Handler
    from OrderService.app.core.config import startup
    await startup()

    # adding routers
    from OrderService.app.api.v1 import router as v1_router
    app.include_router(v1_router)

    yield

    # On Shutdown Event Handler
    from OrderService.app.core.config import shutdown
    await shutdown()


order_app = FastAPI(title='Order Service',
                    docs_url='/order/api/docs',
                    description='Manages the entire lifecycle of an order. ',
                    lifespan=lifespan)
from OrderService.app.core.exceptions import ExceptionMiddleware

order_app.add_middleware(ExceptionMiddleware)
