import logging
import traceback

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error("Unhandled error in middleware:")
            logger.error(traceback.format_exc())
            return HTTPException(
                status_code=500,
                detail={"error": "Something went wrong on our end"},
            )
