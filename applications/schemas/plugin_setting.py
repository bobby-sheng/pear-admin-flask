from applications.extensions import ma
from marshmallow import fields, validate


class pluginSettingInSchema(ma.Schema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)

class pluginSettingOutSchema(ma.Schema):
    key = fields.Str(attribute="key")
    value = fields.Str(rattribute="value")
