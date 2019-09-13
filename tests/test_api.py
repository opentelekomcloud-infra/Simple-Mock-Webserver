"""API tests"""
import uuid


def test_list(session, random_data, entity_uuid):
    response = session.get("/entities")
    assert response.status_code == 200
    entities = response.json()
    assert entity_uuid in [e["uuid"] for e in entities]
    entity = [ent for ent in entities if ent["uuid"] == entity_uuid][0]
    assert entity["data"] == random_data


def test_create(session, random_data):
    response = session.post("/entity", json={"data": random_data})
    assert response.status_code == 201
    location: str = response.headers["Location"]
    assert "/entity/" in location
    _uuid = location.rsplit("/", 1)[1]
    assert str(uuid.UUID(_uuid)) == _uuid


def test_create_400(session):
    response = session.post("/entity")
    print(response.text)
    assert response.status_code == 400


def test_get(session, entity_uuid, random_data):
    entity_data = session.get(f"/entity/{entity_uuid}").json()
    assert entity_data == {"uuid": entity_uuid, "data": random_data}
