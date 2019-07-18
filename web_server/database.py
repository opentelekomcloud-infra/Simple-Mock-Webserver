from uuid import uuid4

from peewee import DatabaseProxy, Model, PostgresqlDatabase, SqliteDatabase, TextField, UUIDField

from web_server.configuration import CONFIGURATION, EntityStruct

DB = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = DB


class Entity(BaseModel):
    """Some stub entity"""

    uuid = UUIDField()
    data = TextField()


def _init_db():
    if CONFIGURATION.DEBUG:
        database = SqliteDatabase("debug.db")
    else:
        database = PostgresqlDatabase(CONFIGURATION.DB_NAME,
                                      host=CONFIGURATION.DB_HOST,
                                      port=CONFIGURATION.DB_PORT,
                                      username=CONFIGURATION.DB_USERNAME,
                                      password=CONFIGURATION.DB_PASSWORD)

    DB.initialize(database)


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
