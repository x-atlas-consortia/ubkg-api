import pytest
from app import app


@pytest.fixture()
def get_app():
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(get_app):
    return app.test_client()


def test_valueset(client):
    response = client.get("/valueset", query_string={'parent_sab': 'SENNET', 'parent_code': 'C000012', 'child_sabs': 'SENNET'})
    assert b'[{"code":"C050002","sab":"SENNET","term":"Dataset"},{"code":"C050003","sab":"SENNET","term":"Sample"},{"code":"C050004","sab":"SENNET","term":"Source"}]' in response.data