import asyncpg


class AsyncPostgresSQLDB:
    _instance = None
    _pool = None
    # Can be configured with env variables
    DEFAULT_PORT = 5432
    MIN_POOL_SIZE = 1
    MAX_POOL_SIZE = 10

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(AsyncPostgresSQLDB, cls).__new__(cls)
        return cls._instance

    async def initialize(self, db_config):
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
                host=db_config["host"],
                port=db_config.get("port", self.DEFAULT_PORT),
                min_size=self.MIN_POOL_SIZE,
                max_size=self.MAX_POOL_SIZE
            )

    async def fetch(self, query, *args):
        async with self._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query, *args):
        async with self._pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def close(self):
        if self._pool:
            await self._pool.close()
