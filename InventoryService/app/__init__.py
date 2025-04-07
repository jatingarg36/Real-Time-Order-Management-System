from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Startup Event Handler
    from InventoryService.app.core.config import startup
    await startup()

    # adding routers
    from InventoryService.app.api.v1 import router as v1_router
    app.include_router(v1_router)

    yield

    # On Shutdown Event Handler
    from InventoryService.app.core.config import shutdown
    await shutdown()


inventory_app = FastAPI(title='Inventory Service',
                        docs_url='/inventory/api/docs',
                        description='Manages the entire lifecycle of a store.',
                        lifespan=lifespan)
from InventoryService.app.core.exceptions import ExceptionMiddleware

inventory_app.add_middleware(ExceptionMiddleware)
