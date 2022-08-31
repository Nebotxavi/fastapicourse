from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello world'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'test_kuma@gmail.com', 'password': 'password123'})

    # this will test the response has the right variables
    new_user = schemas.UserRes(**res.json())
    assert new_user.email == 'test_kuma@gmail.com'
    assert res.status_code == 201
