import pytest
from datetime import datetime
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from core.models.students import Student
from core.models.teachers import Teacher
from core.apis.decorators import AuthPrincipal
from core.libs.exceptions import FyleError
from core import db


@pytest.fixture(scope='function')
def session():
    db.session.begin_nested()
    yield db.session
    db.session.rollback()

# Use this fixture in your tests
def test_submit_assignment(session):
   
    def test_assignment_repr():
        assignment = Assignment(id=1, student_id=1, content="Test content")
        assert repr(assignment) == '<Assignment 1>'

    def test_get_all_assignments():
      
        assignment1 = Assignment(student_id=1, content="Test 1")
        assignment2 = Assignment(student_id=2, content="Test 2")
        db.session.add(assignment1)
        db.session.add(assignment2)
        db.session.commit()

        all_assignments = Assignment.get_all_assignments()
        assert len(all_assignments) >= 2
        assert assignment1 in all_assignments
        assert assignment2 in all_assignments

    def test_get_assignments_by_teacher():
        teacher = Teacher(user_id=1)
        db.session.add(teacher)
        db.session.commit()

        assignment = Assignment(student_id=1, teacher_id=teacher.id, content="Test")
        db.session.add(assignment)
        db.session.commit()

        teacher_assignments = Assignment.get_assignments_by_teacher()
        assert assignment in teacher_assignments

    def test_get_submitted_and_graded_assignments():
 
        draft_assignment = Assignment(student_id=1, content="Draft", state=AssignmentStateEnum.DRAFT)
        submitted_assignment = Assignment(student_id=1, content="Submitted", state=AssignmentStateEnum.SUBMITTED)
        graded_assignment = Assignment(student_id=1, content="Graded", state=AssignmentStateEnum.GRADED)
        
        db.session.add_all([draft_assignment, submitted_assignment, graded_assignment])
        db.session.commit()

        filtered_assignments = Assignment.get_submitted_and_graded_assignments()
        assert draft_assignment not in filtered_assignments
        assert submitted_assignment in filtered_assignments
        assert graded_assignment in filtered_assignments

    def test_submit_assignment_invalid_student():
        assignment = Assignment(id=1, student_id=1, content="Test")
        db.session.add(assignment)
        db.session.commit()

        with pytest.raises(FyleError, match='This assignment belongs to some other student'):
            Assignment.submit(1, 1, AuthPrincipal(student_id=2))

    def test_submit_assignment_empty_content():
        assignment = Assignment(id=1, student_id=1)
        db.session.add(assignment)
        db.session.commit()

        with pytest.raises(FyleError, match='assignment with empty content cannot be submitted'):
            Assignment.submit(1, 1, AuthPrincipal(student_id=1))

    def test_mark_grade_empty_grade():
        assignment = Assignment(id=1, student_id=1, content="Test", state=AssignmentStateEnum.SUBMITTED)
        db.session.add(assignment)
        db.session.commit()

        with pytest.raises(FyleError, match='assignment with empty grade cannot be graded'):
            Assignment.mark_grade(1, None, AuthPrincipal(teacher_id=1))

    def test_upsert_non_draft_assignment():
        assignment = Assignment(id=1, student_id=1, content="Test", state=AssignmentStateEnum.SUBMITTED)
        db.session.add(assignment)
        db.session.commit()

        with pytest.raises(FyleError, match='only assignment in draft state can be edited'):
            Assignment.upsert(Assignment(id=1, content="Updated"))

    # Test for enum classes
    def test_grade_enum():
        assert GradeEnum.A == 'A'
        assert GradeEnum.B == 'B'
        assert GradeEnum.C == 'C'
        assert GradeEnum.D == 'D'

    def test_assignment_state_enum():
        assert AssignmentStateEnum.DRAFT == 'DRAFT'
        assert AssignmentStateEnum.SUBMITTED == 'SUBMITTED'
        assert AssignmentStateEnum.GRADED == 'GRADED'
    pass

