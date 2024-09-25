from flask import Blueprint, request
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum , GradeEnum
from .schema import AssignmentSchema
from core import db

from core.libs import helpers, assertions

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of all submitted and graded assignments"""
    assignments = Assignment.get_submitted_and_graded_assignments()
    
    all_assignments = Assignment.get_all_assignments()
    print(f"Total assignments: {len(all_assignments)}")
    for assignment in all_assignments:
        print(f"ID: {assignment.id}, State: {assignment.state}, Grade: {assignment.grade}")
    
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'])
@decorators.authenticate_principal
def grade_assignment(p):
    """Grade or re-grade an assignment"""
    grade_request = request.get_json()
    assignment_id = grade_request.get('id')
    grade = grade_request.get('grade')

    assertions.assert_valid(assignment_id, 'Assignment ID is required')
    assertions.assert_valid(grade, 'Grade is required')
    assertions.assert_valid(grade in GradeEnum.__members__, 'Invalid grade')

    assignment = Assignment.get_by_id(assignment_id)
    assertions.assert_found(assignment, 'No assignment with this id was found')

    assignment.grade = GradeEnum[grade]
    assignment.state = 'GRADED'  
    assignment.updated_at = helpers.get_utc_now()
    
    db.session.commit()

    return APIResponse.respond(data=AssignmentSchema().dump(assignment))