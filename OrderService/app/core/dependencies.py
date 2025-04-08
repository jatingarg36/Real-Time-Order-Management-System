import redis
from starlette.requests import Request


async def get_redis_client(request: Request) -> redis.Redis:
    redis_client = getattr(request.app.state, 'redis_client', None)
    if not redis_client:
        raise None
    return redis_client
