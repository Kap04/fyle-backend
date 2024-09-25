import pytest
from datetime import datetime
from core.models.students import Student
from core import db

def test_student_creation():
    student = Student(user_id=1)
    assert student.user_id == 1
    assert student.created_at is not None
    assert student.updated_at is not None

def test_student_repr():
    student = Student(id=1, user_id=1)
    assert repr(student) == '<Student 1>'

def test_student_timestamps():
    student = Student(user_id=1)
    db.session.add(student)
    db.session.commit()

    assert isinstance(student.created_at, datetime)
    assert isinstance(student.updated_at, datetime)

    original_updated_at = student.updated_at

    # Simulate an update
    student.user_id = 2
    db.session.commit()

    assert student.updated_at > original_updated_at

def test_student_user_id_foreign_key():
    with pytest.raises(Exception): 
        student = Student(user_id=999999)  
        db.session.add(student)
        db.session.commit()

@pytest.mark.parametrize("field", ["id", "user_id", "created_at", "updated_at"])
def test_student_fields_existence(field):
    assert hasattr(Student, field)

def test_student_tablename():
    assert Student.__tablename__ == 'students'