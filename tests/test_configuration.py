import os
import random
import string

import pytest
import yaml
from jinja2 import Environment, PackageLoader

from too_simple_server.configuration import load_configuration, write_configuration


def _rand_str():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(10))


@pytest.fixture
def debug():
    return random.choice([True, False])


@pytest.fixture
def server_port():
    return random.randrange(0, 0xffff)


@pytest.fixture
def pg_db_url():
    return _rand_str()


@pytest.fixture
def pg_database():
    return _rand_str()


@pytest.fixture
def pg_username():
    return _rand_str()


@pytest.fixture()
def pg_password():
    return _rand_str()


J2_ENV = Environment(loader=PackageLoader("tests"))


@pytest.fixture
def rand_path():
    random_path = _rand_str()
    open(random_path, "w+").close()
    yield random_path
    os.remove(random_path)


@pytest.fixture
def config_file(rand_path, debug, server_port, pg_db_url, pg_database, pg_username, pg_password):
    template = J2_ENV.get_template("config.yml.j2")
    data = template.render(
        debug=debug,
        server_port=server_port,
        pg_db_url=pg_db_url,
        db_name=pg_database,
        db_username=pg_username,
        db_password=pg_password,
    )

    with open(rand_path, "w+") as targ:
        targ.write(data)
    return rand_path


def test_load_cfg(config_file, debug, server_port, pg_db_url, pg_database, pg_username, pg_password):
    args = locals().copy()
    args.pop("config_file")
    config = load_configuration(config_file).to_dict()
    for key, value in args.items():
        assert config[key] == value


def test_write_cfg(rand_path, debug, server_port, pg_db_url, pg_database, pg_username, pg_password):
    args = locals().copy()
    args.pop("rand_path")
    write_configuration(rand_path, **args)
    with open(rand_path) as cfg:
        config_dict = yaml.safe_load(cfg)
    for key, value in config_dict.items():
        assert value == args[key]
