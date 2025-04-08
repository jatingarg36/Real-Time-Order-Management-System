import asyncio

from InventoryService.app.core.kafka.consumer import new_order_consumer
from InventoryService.app.core.kafka.producer import get_kafka_producer
from InventoryService.app.db.connections import AsyncPostgresSQLDB

db = AsyncPostgresSQLDB()


async def startup():
    await db.initialize({
        "user": "workspace",
        "password": "",
        "database": "test_db",
        "host": "localhost",
        "port": 5432
    })
    asyncio.create_task(new_order_consumer())


async def shutdown():
    await db.close()
    producer = await get_kafka_producer()
    await producer.flush()
