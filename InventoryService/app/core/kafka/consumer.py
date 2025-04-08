import json

from aiokafka import AIOKafkaConsumer

from InventoryService.app.constants.order_status import OrderStatus
from InventoryService.app.core.kafka.producer import get_kafka_producer
from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.app.db.crud import update_item_quantity
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def new_order_consumer():
    consumer = AIOKafkaConsumer(
        config.ORDER_PLACE_KAFKA_TOPIC,
        bootstrap_servers=config.KAFKA_SERVER,
    )
    producer = await get_kafka_producer()
    await consumer.start()
    try:
        async for msg in consumer:
            new_order = json.loads(msg.value.decode('utf-8'))
            print(f"Received Order: {new_order}")

            order_items = new_order.get("items", [])
            print(order_items)

            low_quantity_items = []
            try:
                low_quantity_items = await update_item_quantity.action(order_items)
                await producer.send_and_wait(
                    topic=config.ORDER_STATUS_UPDATE_KAFKA_TOPIC,
                    value=json.dumps({
                        "order_id": new_order["order_id"],
                        "status": OrderStatus.PLACED.value
                    }).encode("utf-8")
                )
            except (ValueError, Exception) as e:
                await producer.send_and_wait(
                    topic=config.ORDER_STATUS_UPDATE_KAFKA_TOPIC,
                    value=json.dumps({
                        "order_id": new_order["order_id"],
                        "status": OrderStatus.FAILED.value,
                        "reason": str(e)
                    }).encode("utf-8")
                )
            if len(low_quantity_items) > 0:
                print("Low Quantity Items:", low_quantity_items)
                await producer.send_and_wait(
                    topic=config.STOCK_DEFICIENT_ALERT_KAFKA_TOPIC,
                    value=json.dumps([{'item_id': item_id} for item_id in low_quantity_items]).encode("utf-8")
                )
    finally:
        await consumer.stop()


async def cancel_order_consumer():
    consumer = AIOKafkaConsumer(
        config.ORDER_CANCEL_KAFKA_TOPIC,
        bootstrap_servers=config.KAFKA_SERVER,
    )
    producer = await get_kafka_producer()
    await consumer.start()
    try:
        async for msg in consumer:
            order = json.loads(msg.value.decode('utf-8'))
            print(f"Received Order: {order}")
            order_items = order.get('items', [])
            if len(order_items) > 0:
                # reversing the quantity
                order_items = [item.update({'quantity': -1 * item['quantity']}) for item in order_items]
                await update_item_quantity.action(order_items)
                await producer.send_and_wait(
                    topic=config.ORDER_STATUS_UPDATE_KAFKA_TOPIC,
                    value=json.dumps({
                        "order_id": order["order_id"],
                        "status": OrderStatus.CANCELLED.value
                    }).encode("utf-8")
                )
    finally:
        await consumer.stop()
