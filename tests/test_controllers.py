import json

import pytest
from app import app


@pytest.fixture()
def get_app():
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(get_app):
    return app.test_client()


def assertExpectedResponseEqualsActualResponse(response, expected_response_file_name):
    with open(expected_response_file_name) as f:
        expected = json.loads(f.read())
    actual = response.get_json()
    assert expected == actual


def test_datasets(client):
    response = client.get('/datasets', query_string={'application_context': 'SENNET'})
    assertExpectedResponseEqualsActualResponse(response, 'expected_responses/datasets.json')


def test_valuest_sennet_organs(client):
    response = client.get('/organs', query_string={'application_context': 'SENNET'})
    assertExpectedResponseEqualsActualResponse(response, 'expected_responses/valueset_organs.json')


def test_valueset_sennet_entities(client):
    response = client.get('/valueset',
                          query_string={'child_sabs': 'SENNET', 'parent_sab': 'SENNET', 'parent_code': 'C000012'})
    assertExpectedResponseEqualsActualResponse(response, 'expected_responses/valueset_entities.json')


def test_valueset_sennet_specimen_categories(client):
    response = client.get('/valueset',
                          query_string={'child_sabs': 'SENNET', 'parent_sab': 'SENNET', 'parent_code': 'C020076'})
    assertExpectedResponseEqualsActualResponse(response, 'expected_responses/valueset_specimen_categories.json')


def test_valueset_sennet_source_types(client):
    response = client.get('/valueset',
                          query_string={'child_sabs': 'SENNET', 'parent_sab': 'SENNET', 'parent_code': 'C050020'})
    assertExpectedResponseEqualsActualResponse(response, 'expected_responses/valueset_source_types.json')
