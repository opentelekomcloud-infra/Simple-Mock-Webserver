from uuid import uuid4

from peewee import DatabaseProxy, Model, PostgresqlDatabase, SqliteDatabase, TextField, UUIDField

from .configuration import EntityStruct, load_configuration

DB = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = DB


class Entity(BaseModel):
    """Some stub entity"""

    uuid = UUIDField()
    data = TextField()


def init_db():
    configuration = load_configuration()
    if configuration.debug:
        database = SqliteDatabase("debug.db")
    else:
        host, port = configuration.pg_bd_url.split(":")
        database = PostgresqlDatabase(configuration.pg_database,
                                      host=host,
                                      port=port,
                                      username=configuration.pg_username,
                                      password=configuration.pg_password)

    DB.initialize(database)
    if not database.table_exists(Entity.__name__):
        database.create_tables([Entity])


def create_entity(data: EntityStruct) -> str:
    """Create new entity returning uuid of created record"""
    new_uuid = str(uuid4())
    Entity.create(uuid=new_uuid, data=data.data)
    return new_uuid


def get_entity_data(uuid: str) -> dict:
    entity: Entity = Entity.get(uuid=uuid)
    return EntityStruct(data=entity.data)._asdict()


def get_all_enities() -> dict:
    all_ent = Entity.select()
    return {str(ent.uuid): EntityStruct(data=ent.data)._asdict() for ent in all_ent}
