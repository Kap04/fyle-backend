import pytest
from unittest.mock import patch, MagicMock
from core.models.teachers import Teacher
from core.apis.responses import APIResponse

def test_list_teachers_success(client, h_principal):
    # Mock the Teacher.query.all() method
    with patch('core.models.teachers.Teacher.query') as mock_query:
        mock_teachers = [Teacher(id=1, name='Teacher 1'), Teacher(id=2, name='Teacher 2')]
        mock_query.all.return_value = mock_teachers

        response = client.get('/principal/teachers', headers=h_principal)

        assert response.status_code == 200
        data = response.json['data']
        assert len(data) == 2
        assert data[0]['id'] == 1
        assert data[0]['name'] == 'Teacher 1'
        assert data[1]['id'] == 2
        assert data[1]['name'] == 'Teacher 2'

def test_list_teachers_empty(client, h_principal):
    # Mock the Teacher.query.all() method to return an empty list
    with patch('core.models.teachers.Teacher.query') as mock_query:
        mock_query.all.return_value = []

        response = client.get('/principal/teachers', headers=h_principal)

        assert response.status_code == 200
        assert response.json['data'] == []

def test_list_teachers_unauthorized(client):
    response = client.get('/principal/teachers')
    assert response.status_code == 401

@pytest.mark.parametrize('api_response', [
    {'status': 'success', 'data': [{'id': 1, 'name': 'Teacher 1'}]},
    {'status': 'error', 'message': 'An error occurred'},
])
def test_api_response(client, h_principal, api_response):
    with patch('core.apis.responses.APIResponse.respond') as mock_respond:
        mock_respond.return_value = api_response

        response = client.get('/principal/teachers', headers=h_principal)

        assert response.status_code == 200
        assert response.json == api_response