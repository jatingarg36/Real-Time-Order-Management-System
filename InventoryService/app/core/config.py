import asyncio

from InventoryService.app.core.kafka.consumer import new_order_consumer
from InventoryService.app.core.kafka.producer import get_kafka_producer
from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def startup():
    await db.initialize({
        "user": config.DB_USER,
        "password": config.DB_PASSWORD,
        "database": config.DB_NAME,
        "host": config.DB_HOST,
        "port": config.DB_PORT
    })
    asyncio.create_task(new_order_consumer())


async def shutdown():
    await db.close()
    producer = await get_kafka_producer()
    await producer.flush()
