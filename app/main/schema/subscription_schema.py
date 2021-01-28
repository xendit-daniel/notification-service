from marshmallow import Schema, fields, post_load, ValidationError, validate
from uuid import UUID

from app.main.model.subscription import Subscription

class SubscriptionBaseSchema(Schema):
    id = fields.Integer()
    customer_id = fields.Integer(allow_none=False, required=True)
    subscription_key = fields.UUID(dump_only=True)
    callback_url = fields.Url(allow_none=False, required=True)
    created_date = fields.DateTime(dump_only=True)
    last_update = fields.DateTime(dump_only=True)
    
    class Meta:
        model = Subscription
        strict = True
 
    @post_load
    def save_object(self, data, **kwargs):
        return Subscription(**data)
