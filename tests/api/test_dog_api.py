import pytest
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_list_dogs():
    response = client.get('/dog/list/')
    assert response.data == []
    assert response.status_code == 200

    response = client.post('/dog/populate/', {})
    response = client.get('/dog/list/')
    assert len(response.data) == 12
    assert response.status_code == 200

@pytest.mark.django_db
def test_populate_dogs():
    response = client.post('/dog/populate/', {})
    assert response.status_code == 201
    response = client.get('/dog/list/')
    assert len(response.data) == 12
    assert response.status_code == 200

@pytest.mark.django_db
def test_show_dog():
    response = client.post('/dog/populate/', {})
    assert response.status_code == 201
    response = client.get('/dog/show/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_dog_pair_by_id():
    response = client.post('/dog/populate/', {})
    assert response.status_code == 201

    response = client.get('/dog/list/')

    response = client.get(f'/dog/show/{response.data[0]["uuid"]}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_dog():
    response = client.post('/dog/populate/', {})
    assert response.status_code == 201

    response = client.get('/dog/list/')

    response = client.delete(f'/dog/delete/{response.data[0]["uuid"]}/')
    assert response.status_code == 204
