import pytest
from core.models.assignments import Assignment
from core.apis.responses import APIResponse

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_success(client, h_teacher_1):
    """
    success case: grade a submitted assignment
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 200
    data = response.json['data']
    assert data['grade'] == 'A'
    assert data['state'] == 'GRADED'


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_get_assignments_no_assignments(client, h_teacher_1, mocker):
    """
    Test case when a teacher has no assignments
    """
    mocker.patch('core.models.assignments.Assignment.get_assignments_by_teacher', return_value=[])
    
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200
    assert response.json['data'] == []


@pytest.mark.parametrize('invalid_payload', [
    {},
    {'id': 1},
    {'grade': 'A'},
    {'id': 'invalid', 'grade': 'A'},
    {'id': 1, 'grade': 123},
])
def test_grade_assignment_invalid_payload(client, h_teacher_1, invalid_payload):
    """
    Test various invalid payloads for grading assignments
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json=invalid_payload
    )

    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'