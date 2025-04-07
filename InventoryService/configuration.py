import os
import pathlib

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv(verbose=True, override=True)

BRANCH = os.environ.get('branch')
if BRANCH == "develop":
    base_dir = pathlib.Path(__file__).parent
    load_dotenv(base_dir, override=True)
    response_secrets = {k: v for k, v in os.environ.items()}


class GlobalConfig(BaseSettings):
    DB_NAME: str = response_secrets["DB_NAME"]
    INVENTORY_TABLE_NAME: str = response_secrets["INVENTORY_TABLE_NAME"]


config = GlobalConfig()

