"""Configuration consts"""
import os
from dataclasses import asdict, dataclass
from typing import NamedTuple, Optional

import yaml

DEFAULT_CFG_PATH = "/etc/too-simple/config.yml"


@dataclass
class Configuration:
    """Default values for configuration"""

    debug: bool = True

    server_port: int = 5054

    pg_db_url: str = "localhost:9999"
    pg_database: str = "entities"
    pg_username: str = "entities"
    pg_password: Optional[str] = None

    def to_dict(self):
        """Return fields dict for instance"""
        return asdict(self)


DEFAULTS = Configuration()


def write_configuration(path=DEFAULT_CFG_PATH, **kwargs):
    """Writes configuration to configuration file"""

    config_data = DEFAULTS.to_dict()
    kwargs = {k: v for k, v in kwargs.items() if k in config_data}  # filter possible keys
    if not kwargs:
        return  # exit if there nothing to configure
    if os.path.exists(path):
        with open(path) as r_cfg_file:
            config_data = yaml.safe_load(r_cfg_file)
        if config_data is None:
            config_data = {}
    config_data.update(**kwargs)
    with open(path, "w+") as w_cfg_file:
        w_cfg_file.write(yaml.safe_dump(config_data))


def load_configuration(path: str = DEFAULT_CFG_PATH) -> Configuration:
    """Load configuration from given path"""
    config_data = DEFAULTS.to_dict()
    if os.path.exists(path):
        with open(path) as r_cfg_file:
            config_data = yaml.safe_load(r_cfg_file)
    else:
        print("No configuration file found. Default configuration will be used")
    return Configuration(**config_data)


class EntityStruct(NamedTuple):
    uuid: str
    data: str


_IN_USER_DIR = os.path.expanduser("~/.too-simple")


def _try_dir(default, fallback):
    file_name = f"{default}/randomfilename"
    try:
        os.makedirs(default, exist_ok=True)
        open(file_name, "w+").close()
        os.remove(file_name)
        return default
    except (IOError, PermissionError):
        os.makedirs(fallback, exist_ok=True)
        return fallback
