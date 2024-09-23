import pytest
from flask import Flask, request, jsonify
from core.apis.decorators import AuthPrincipal, accept_payload, authenticate_principal
from core.libs.exceptions import FyleError
import json

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_auth_principal_initialization():
    auth = AuthPrincipal(user_id=1, student_id=2, teacher_id=3, principal_id=4)
    assert auth.user_id == 1
    assert auth.student_id == 2
    assert auth.teacher_id == 3
    assert auth.principal_id == 4

def test_accept_payload_decorator(app):
    @app.route('/test', methods=['POST'])
    @accept_payload
    def test_func(payload):
        return jsonify(payload)

    with app.test_client() as client:
        response = client.post('/test', json={'key': 'value'})
        assert response.status_code == 200
        assert response.json == {'key': 'value'}

def test_authenticate_principal_decorator_student(app):
    @app.route('/student/test')
    @authenticate_principal
    def test_func(p):
        return jsonify({'user_id': p.user_id, 'student_id': p.student_id})

    with app.test_client() as client:
        headers = {'X-Principal': json.dumps({'user_id': 1, 'student_id': 2})}
        response = client.get('/student/test', headers=headers)
        assert response.status_code == 200
        assert response.json == {'user_id': 1, 'student_id': 2}

def test_authenticate_principal_decorator_teacher(app):
    @app.route('/teacher/test')
    @authenticate_principal
    def test_func(p):
        return jsonify({'user_id': p.user_id, 'teacher_id': p.teacher_id})

    with app.test_client() as client:
        headers = {'X-Principal': json.dumps({'user_id': 1, 'teacher_id': 3})}
        response = client.get('/teacher/test', headers=headers)
        assert response.status_code == 200
        assert response.json == {'user_id': 1, 'teacher_id': 3}

def test_authenticate_principal_decorator_principal(app):
    @app.route('/principal/test')
    @authenticate_principal
    def test_func(p):
        return jsonify({'user_id': p.user_id, 'principal_id': p.principal_id})

    with app.test_client() as client:
        headers = {'X-Principal': json.dumps({'user_id': 1, 'principal_id': 4})}
        response = client.get('/principal/test', headers=headers)
        assert response.status_code == 200
        assert response.json == {'user_id': 1, 'principal_id': 4}

def test_authenticate_principal_decorator_missing_header(app):
    @app.route('/test')
    @authenticate_principal
    def test_func(p):
        return jsonify({'user_id': p.user_id})

    with app.test_client() as client:
        with pytest.raises(FyleError) as exc_info:
            client.get('/test')
        assert 'principal not found' in str(exc_info.value)

def test_authenticate_principal_decorator_invalid_role(app):
    @app.route('/invalid/test')
    @authenticate_principal
    def test_func(p):
        return jsonify({'user_id': p.user_id})

    with app.test_client() as client:
        headers = {'X-Principal': json.dumps({'user_id': 1})}
        with pytest.raises(FyleError) as exc_info:
            client.get('/invalid/test', headers=headers)
        assert 'No such api' in str(exc_info.value)

def test_authenticate_principal_decorator_wrong_role(app):
    @app.route('/student/test')
    @authenticate_principal
    def test_func(p):
        return jsonify({'user_id': p.user_id, 'student_id': p.student_id})

    with app.test_client() as client:
        headers = {'X-Principal': json.dumps({'user_id': 1, 'teacher_id': 3})}
        with pytest.raises(FyleError) as exc_info:
            client.get('/student/test', headers=headers)
        assert 'requester should be a student' in str(exc_info.value)