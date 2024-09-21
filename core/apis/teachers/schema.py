from marshmallow import Schema, fields

class TeacherSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)