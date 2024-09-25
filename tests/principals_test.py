from core.models.assignments import AssignmentStateEnum, GradeEnum
import pytest



def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_grade_submitted_assignment(client, h_principal):
    """Test grading a submitted assignment"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,  
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B.value

def test_grade_assignment_invalid_grade(client, h_principal):
    """Test grading with an invalid grade"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,
            'grade': 'INVALID_GRADE'
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'ValidationError'

def test_grade_nonexistent_assignment(client, h_principal):
    """Test grading a nonexistent assignment"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 9999,  
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'FyleError'

def test_grade_already_graded_assignment(client, h_principal):
    """Test grading an already graded assignment"""
    
    client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.A.value

@pytest.mark.parametrize("grade", list(GradeEnum))
def test_grade_assignment_all_grades(client, h_principal, grade):
    """Test grading with all possible grades"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,  
            'grade': grade.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == grade.value
