from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            raise e
        except Exception as exc:
            return HTTPException(
                status_code=500,
                detail={"error": "internal service error"},
            )
