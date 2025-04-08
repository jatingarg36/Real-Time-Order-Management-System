import json

import redis

from OrderService.configuration import config


def load_inventory_cache(app):
    redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)
    redis_client.hset(config.INVENTORY_REDIS_KEY, str('83e9e017-4f03-4491-a6ea-1c813d1fb2b3'),
                      json.dumps({'item_name': 'burger'}))
    redis_client.hset(config.INVENTORY_REDIS_KEY, str('9f548ff6-821b-4271-afd1-868a4c72d6ce'),
                      json.dumps({'item_name': 'pizza'}))
    app.state.redis_client = redis_client
