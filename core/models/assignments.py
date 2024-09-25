import enum
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.libs.exceptions import FyleError
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum
from sqlalchemy.exc import SQLAlchemyError


class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_data):
        try:
            if assignment_data.id:
                assignment = cls.query.get(assignment_data.id)
                if assignment and assignment.state != AssignmentStateEnum.DRAFT:
                    raise FyleError(error_message="only assignment in draft state can be edited")
            else:
                assignment = cls()

            for key, value in assignment_data.__dict__.items():
                if hasattr(assignment, key):
                    setattr(assignment, key, value)

            db.session.add(assignment)
            db.session.commit()
            return assignment
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @classmethod
    def submit(cls, _id, teacher_id, auth_principal):
        try:
            assignment = cls.query.get(_id)
            if not assignment:
                raise FyleError(error_message="Assignment not found")
            if assignment.student_id != auth_principal.student_id:
                raise FyleError(error_message="This assignment belongs to some other student")
            if not assignment.content:
                raise FyleError(error_message="assignment with empty content cannot be submitted")
            
            assignment.teacher_id = teacher_id
            assignment.state = AssignmentStateEnum.SUBMITTED
            db.session.commit()
            return assignment
        except SQLAlchemyError:
            db.session.rollback()
            raise



    @classmethod
    def mark_grade(cls, _id, grade, auth_principal):
        try:
            assignment = cls.query.get(_id)
            if not assignment:
                raise FyleError(error_message="Assignment not found")
            if not grade:
                raise FyleError(error_message="assignment with empty grade cannot be graded")
            
            assignment.grade = grade
            assignment.state = AssignmentStateEnum.GRADED
            db.session.commit()
            return assignment
        except SQLAlchemyError:
            db.session.rollback()
            raise


    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()

    @classmethod
    def get_assignments_by_teacher(cls):
        return cls.query.all()
    
    @classmethod
    def get_submitted_and_graded_assignments(cls):
        return cls.filter(
            cls.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
        ).all()

    @classmethod
    def get_all_assignments(cls):
        return cls.query.all()

    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        return cls.filter(
            cls.teacher_id == teacher_id,
            cls.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
        ).all()

    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.teacher_id == auth_principal.teacher_id, 'This assignment belongs to another teacher')
        assertions.assert_valid(assignment.state == AssignmentStateEnum.SUBMITTED, 'Only submitted assignments can be graded')
        assertions.assert_valid(grade is not None, 'Assignment with empty grade cannot be graded')

        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()

        return assignment
