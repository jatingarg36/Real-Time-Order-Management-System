import json
from typing import List

from OrderService.app.core.kafka.producer import get_kafka_producer
from OrderService.app.db.models.order import Order, OrderItems
from OrderService.configuration import config


async def send_order_to_kafka(order: Order, order_item: List[OrderItems]):
    producer = await get_kafka_producer()

    new_order_payload = {
        "order_id": str(order.order_id),
        "user_id": str(order.user_id),
        "items": [{'item_id': str(item.item_id), 'quantity': item.quantity} for item in order_item]
    }
    await producer.send_and_wait(
        topic=config.ORDER_PLACE_KAFKA_TOPIC,
        value=json.dumps(new_order_payload).encode("utf-8")
    )
