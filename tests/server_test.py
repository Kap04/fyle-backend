import pytest
from flask import json
from core import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_ready_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ready'
    assert 'time' in data

def test_fyle_error_handler(client):
    @app.route('/test-fyle-error')
    def raise_fyle_error():
        raise FyleError('Test FyleError', status_code=422)

    response = client.get('/test-fyle-error')
    assert response.status_code == 422
    data = json.loads(response.data)
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Test FyleError'

def test_validation_error_handler(client):
    @app.route('/test-validation-error')
    def raise_validation_error():
        raise ValidationError('Test ValidationError')

    response = client.get('/test-validation-error')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'ValidationError'
    assert 'Test ValidationError' in str(data['message'])

def test_integrity_error_handler(client):
    @app.route('/test-integrity-error')
    def raise_integrity_error():
        raise IntegrityError(None, None, None)

    response = client.get('/test-integrity-error')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'IntegrityError'

def test_http_exception_handler(client):
    response = client.get('/non-existent-route')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'NotFound'

def test_unhandled_exception(client):
    @app.route('/test-unhandled-exception')
    def raise_unhandled_exception():
        raise ValueError('Test unhandled exception')

    with pytest.raises(ValueError, match='Test unhandled exception'):
        client.get('/test-unhandled-exception')

def test_main_not_called(monkeypatch):
    
    mock_run = monkeypatch.Mock()
    monkeypatch.setattr(app, 'run', mock_run)
    
    exec(open('core/server.py').read())

    mock_run.assert_not_called()
