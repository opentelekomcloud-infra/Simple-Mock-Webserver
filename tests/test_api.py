"""API tests"""
import uuid


def test_list(session, random_data, entity):
    entities = session.get("/entities").json()  # type: dict
    assert entity in entities
    assert entities[entity]["data"] == random_data


def test_create(session, random_data):
    response = session.post("/entity", json={"data": random_data})
    assert response.status_code == 201
    location: str = response.headers["Location"]
    assert "/entity/" in location
    _uuid = location.rsplit("/", 1)[1]
    assert str(uuid.UUID(_uuid)) == _uuid


def test_get(session, entity, random_data):
    entity_data = session.get(f"/entity/{entity}").json()
    assert entity_data == {"data": random_data}
