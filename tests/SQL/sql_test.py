import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    # Iterate over each assignment and update its state
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Define the expected result before any changes
    expected_result = [(1, 3)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Print initial state
    print("Initial state:")
    print_debug_info()

    # Create and grade 5 assignments for teacher 1
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5, teacher_id=1)
    print(f"Created {grade_a_count_1} grade A assignments for teacher 1")

    # Create fewer grade A assignments for teacher 2 to ensure teacher 1 has the max
    grade_a_count_2 = create_n_graded_assignments_for_teacher(3, teacher_id=2)
    print(f"Created {grade_a_count_2} grade A assignments for teacher 2")

    # Print state after creating assignments
    print("After creating assignments:")
    print_debug_info()

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    print(f"SQL query result: {sql_result}")
    assert len(sql_result) == 1, "Expected exactly one result"
    assert sql_result[0][0] == 1, "Expected teacher_id to be 1"
    assert sql_result[0][1] == grade_a_count_1, f"Expected {grade_a_count_1} grade A assignments, got {sql_result[0][1]}"

def print_debug_info():
    all_assignments = Assignment.get_all_assignments()
    print(f"Total assignments: {len(all_assignments)}")
    grade_a_assignments = [a for a in all_assignments if a.grade == GradeEnum.A and a.state == AssignmentStateEnum.GRADED]
    print(f"Total grade A assignments: {len(grade_a_assignments)}")
    teacher_counts = {}
    for a in grade_a_assignments:
        teacher_counts[a.teacher_id] = teacher_counts.get(a.teacher_id, 0) + 1
    print(f"Grade A assignments per teacher: {teacher_counts}")