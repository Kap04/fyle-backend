from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of all submitted and graded assignments"""
    assignments = Assignment.get_submitted_and_graded_assignments()
    
    # Debugging information
    all_assignments = Assignment.get_all_assignments()
    print(f"Total assignments: {len(all_assignments)}")
    for assignment in all_assignments:
        print(f"ID: {assignment.id}, State: {assignment.state}, Grade: {assignment.grade}")
    
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)