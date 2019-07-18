"""Configuration consts"""
import os
from typing import NamedTuple


class CONFIGURATION:
    """Configuration container"""
    DEBUG = True
    SERVER_PORT = int(os.getenv("SERVER_PORT", 5054))

    DB_HOST, DB_PORT = os.getenv("PG_DB_URL", "localhost:9999").split(":")
    DB_NAME = os.getenv("PG_DATABASE", "entities")
    DB_USERNAME = os.getenv("PG_USERNAME", "entities")
    DB_PASSWORD = os.getenv("PG_PASSWORD")

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Don't create instance of CONFIGURATION class")


class EntityStruct(NamedTuple):
    data: str
