from flask import Flask, Response, jsonify, request

from .database import create_entity, get_all_entities, get_entity_data

API = Flask("API")


@API.route("/")
def is_up():
    return "OK"


@API.route("/entity/<uuid>")
def get(uuid):
    """Return some entity"""
    return jsonify(get_entity_data(uuid))


@API.route("/entity", methods=["POST"])
def create():
    """Create new entity"""
    if not request.json or "data" not in request.json:
        return Response(status=400)
    new_id = create_entity(request.json)
    return Response({}, 201, headers={"Location": f"/entity/{new_id}"})


@API.route("/entities")
def list_all():
    """Get list of all entities"""
    return jsonify(get_all_entities())
