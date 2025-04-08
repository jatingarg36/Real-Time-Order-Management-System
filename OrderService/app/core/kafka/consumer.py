import json
from datetime import datetime

from aiokafka import AIOKafkaConsumer

from OrderService.app.db.connections import AsyncPostgresSQLDB
from OrderService.app.db.crud import update_order_status
from OrderService.app.db.models.order import OrderUpdate
from OrderService.configuration import config

db = AsyncPostgresSQLDB()


async def start_order_update_consumer():
    consumer = AIOKafkaConsumer(
        config.ORDER_STATUS_UPDATE_KAFKA_TOPIC,
        bootstrap_servers=config.KAFKA_SERVER,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            order_update = json.loads(msg.value.decode('utf-8'))
            print(f"Received Order Updates: {order_update}")
            order_update = OrderUpdate(order_id=order_update['order_id'], status=order_update['status'],
                                       updated_at=datetime.now(),
                                       reason=order_update.get('reason', None))
            print(order_update)
            await update_order_status.action(order_update)

    finally:
        await consumer.stop()


async def new_item_cache(app):
    consumer = AIOKafkaConsumer(
        config.NEW_ITEM_ALERT_KAFKA_TOPIC,
        bootstrap_servers=config.KAFKA_SERVER,
    )
    redis_client = getattr(app.state, 'redis_client', None)
    if redis_client:
        await consumer.start()
        try:
            async for msg in consumer:
                new_item = json.loads(msg.value.decode('utf-8'))
                print(f"Received Order Updates: {new_item}")
                if isinstance(new_item, str):
                    redis_client.sadd(config.INVENTORY_REDIS_KEY, new_item)

        finally:
            await consumer.stop()
