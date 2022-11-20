import pytest
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_list_keyvalue():
    response = client.get('/incrementer/list/')
    assert response.data == []
    assert response.status_code == 200
    payload = {
        "key": 'test',
        "value": 0
    }

    response = client.post('/incrementer/', payload)
    response = client.get('/incrementer/list/')
    assert len(response.data) == 1
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_keyvalue():
    payload = {
        "key": 'test',
        "value": 0
    }

    response = client.post('/incrementer/', payload)
    data = response.data
    assert response.status_code == 201
    assert data['key'] == payload['key']
    assert data['value'] == payload['value']

@pytest.mark.django_db
def test_create_keyvalue_default_value():
    payload = {
        "key": 'test'
    }

    response = client.post('/incrementer/', payload)
    data = response.data
    assert data['key'] == payload['key']
    assert data['value'] == 0

@pytest.mark.django_db
def test_create_keyvalue_fail():
    payload = {
        "value": 0
    }

    response = client.post('/incrementer/', payload)
    assert response.status_code == 400

@pytest.mark.django_db
def test_delete_keyvalue():
    payload = {
        "key": 'test',
        "value": 1
    }

    response = client.post('/incrementer/', payload)
    response = client.delete(f'/incrementer/key/{payload["key"]}/')
    assert response.status_code == 204

@pytest.mark.django_db
def test_inc_keyvalue():
    payload = {
        "key": 'test',
        "value": 1
    }

    response = client.post('/incrementer/', payload)
    response = client.put(f'/incrementer/inc/{payload["key"]}')
    assert response.status_code == 204

@pytest.mark.django_db
def test_inc_keyvalue_fail():
    payload = {
        "key": 'test',
        "value": 1
    }

    response = client.put('/incrementer/inc/', payload)
    assert response.status_code == 404