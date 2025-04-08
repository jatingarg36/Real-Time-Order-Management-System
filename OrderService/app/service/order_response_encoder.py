from typing import List

from OrderService.app.constants.order_status import OrderStatus
from OrderService.app.schemas.order_schema import OrderResponse, OrderItemResponse


class ResponseEncoder:
    def __init__(self, inventory_cache):
        self.inventory_cache = inventory_cache

    def get_item_name(self, item_id: str) -> str:
        item = self.inventory_cache.hget("item_names", str(item_id))
        if item:
            item_name = item.get("name")
            return item_name or "Unknown Item"
        return "Unknown Item"

    def encode_order_records(self, records: List) -> OrderResponse:
        if not records:
            raise ValueError("No records to encode")

        # Extract shared order data from first record
        first = records[0]
        order_items = []

        for record in records:
            item = OrderItemResponse(
                item_id=record['item_id'],
                item_name=self.get_item_name(record['item_id']),
                quantity=record['quantity'],
            )
            order_items.append(item)

        order = OrderResponse(
            order_id=first['order_id'],
            status=OrderStatus(first['status']),
            user_id=first['user_id'],
            store_id=first['store_id'],
            total_amount=float(first['total_amount']),
            payment_id=first['payment_id'],
            items=order_items,
            created_at=first['created_at'],
            updated_at=first['updated_at'],
        )
        return order
