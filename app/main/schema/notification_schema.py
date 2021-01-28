from marshmallow import Schema, fields, post_load, validate
from uuid import UUID

from app.main.model.notification import Notification

class NotificationBaseSchema(Schema):

    id = fields.Integer()
    public_id = fields.UUID(dump_only=True)
    title = fields.String(allow_none=False, required=True)
    message = fields.String(allow_none=False, required=True)
    created_date = fields.DateTime(dump_only=True)
    last_update = fields.DateTime(dump_only=True)
    subscription_id = fields.Integer(allow_none=False, required=True)
    delivery_status = fields.String(dump_only=True)

    class Meta:
        model = Notification
        strict = True
 
    @post_load
    def save_object(self, data, **kwargs):
        return Notification(**data)

class NotificationStatusSchema(Schema):
    delivery_status = fields.String(
        allow_none=False, 
        required=True,
        validate=validate.OneOf([Notification.IN_PROGRESS, Notification.CANCELLED])
    )

    class Meta:
        model = Notification
        strict = True