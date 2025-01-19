from marshmallow import Schema, fields, validate

class ApartmentSchema(Schema):
    apt_id = fields.Int()
    description = fields.Str(required=True, validate=validate.Length(min=1))
    location = fields.Str(required=True)
    rent = fields.Float(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    utilities = fields.Str()
    university_name = fields.Str(required=True)
    photos = fields.Str()
    contact = fields.Int(required=True)

apartment_schema = ApartmentSchema()

