import json
import uuid
from datetime import datetime
from typing import List

from fastapi import HTTPException
from fastapi_pagination import Params

from OrderService.app.constants.order_status import OrderStatus
from OrderService.app.core.kafka.producer import get_kafka_producer
from OrderService.app.db.crud import save_order, fetch_order, fetch_all_orders
from OrderService.app.db.models.order import Order, OrderItems
from OrderService.app.schemas.order_schema import OrderCreate, OrderResponse
from OrderService.app.service import validate_order
from OrderService.app.service.order_response_encoder import ResponseEncoder
from OrderService.app.service.send_order_kafka import send_order_to_kafka
from OrderService.configuration import config


class OrderManager:
    def __init__(self, inventory_cache):
        self.inventory_cache = inventory_cache
        self.response_encoder = ResponseEncoder(inventory_cache)

    # Step 1: Validate
    # Step 2: Save DB
    # Step 3: publish kafka event for inventory
    async def place_order(self, order: OrderCreate):
        new_order = Order(order_id=uuid.uuid4(),
                          status=OrderStatus.PENDING,
                          user_id=order.user_id,
                          total_amount=order.total_price,
                          # This will be handled while placing the order, and validating it with payment.
                          store_id=order.store_id,
                          payment_id=uuid.uuid4(),
                          created_at=datetime.now(),
                          updated_at=datetime.now())

        order_items = [OrderItems(order_id=new_order.order_id, item_id=item.item_id, quantity=item.quantity)
                       for item in order.items]

        is_valid = await validate_order.action(order_items, self.inventory_cache)
        if is_valid:
            # Creates a new entry for order
            await save_order.action(new_order, order_items)

            # Publish order to kafka topic for further utilisation
            await send_order_to_kafka(new_order, order_items)

            return await fetch_order.action(str(new_order.order_id), str(new_order.user_id),
                                            self.response_encoder.encode_order_records)

        return HTTPException(status_code=400, detail="The items in the orders are invalid")

    async def cancel_order(self, order_id, user_id):
        order = await fetch_order.action(str(order_id), str(user_id), self.response_encoder.encode_order_records)

        producer = await get_kafka_producer()
        producer.send_and_wait(topic=config.ORDER_CANCEL_KAFKA_TOPIC,
                               value=json.dumps(order).encode("utf-8"))

    async def fetch_order(self, user_id, order_id):
        result = await fetch_order.action(str(order_id), str(user_id), self.response_encoder.encode_order_records)
        if result is None:
            raise HTTPException(status_code=404, detail="Invalid order_id")
        return result

    async def fetch_all_orders(self, user_id, params: Params) -> List[OrderResponse]:
        return await fetch_all_orders.action(user_id, params, self.response_encoder.encode_order_records)
