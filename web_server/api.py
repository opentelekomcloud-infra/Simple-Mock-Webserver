from flask import Flask
from flask_restful import Api, Resource

from .database import create_entity, get_all_enities, get_entity_data

SERVER = Flask("mock_server")
API = Api(SERVER)


class MockEntity(Resource):
    """Mock for resource"""

    def get(self, entity_id):
        """Return some entity"""
        return get_entity_data(entity_id)


class MockEntityList(Resource):
    """List of mock entities"""

    def get(self):
        """Get list of all entities"""
        return get_all_enities()

    def post(self, data):
        """Create new entity"""
        return create_entity(data)


API.add_resource(MockEntity, "/entity/<uuid:uuid>")
API.add_resource(MockEntityList, "/entities")
