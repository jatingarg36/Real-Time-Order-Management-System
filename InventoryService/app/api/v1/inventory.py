from typing import List, Optional

from fastapi import APIRouter

from InventoryService.app.core.inventory_handler import InventoryHandler
from InventoryService.app.db.models.inventory import Item
from InventoryService.app.schemas.inventory_schema import ItemCreate, ItemUpdate

router = APIRouter(prefix='/inventory')


@router.get('/all_items', response_model=List[Item],
            description="Retrieve a list of all available items for a specific store.")
async def action(store_id: Optional[str] = None):
    return await InventoryHandler().fetch_items(store_id)


@router.post('/add_item', response_model=Item,
             description="Add a new item to the inventory. Intended for use by store owners.")
async def action(create_item: ItemCreate):
    return await InventoryHandler().add_new_item(create_item)


@router.patch('/update_item', response_model=Item,
              description="Update item details such as quantity, threshold, or price in the inventory. Intended for use by store owners.")
async def action(update_item: ItemUpdate):
    return await InventoryHandler().update_item(update_item)
