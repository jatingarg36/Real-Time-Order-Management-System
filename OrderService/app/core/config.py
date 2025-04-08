import asyncio

from OrderService.app.core.cache import load_inventory_cache
from OrderService.app.core.kafka.consumer import start_order_update_consumer, new_item_cache
from OrderService.app.core.kafka.producer import get_kafka_producer
from OrderService.app.db.connections import AsyncPostgresSQLDB

db = AsyncPostgresSQLDB()


async def startup(app):
    await db.initialize({
        "user": "workspace",
        "password": "",
        "database": "test_db",
        "host": "localhost",
        "port": 5432
    })
    load_inventory_cache(app)
    asyncio.create_task(start_order_update_consumer())
    asyncio.create_task(new_item_cache(app))


async def shutdown(app):
    await db.close()
    app.state.redis_client.close()
    producer = await get_kafka_producer()
    await producer.flush()
