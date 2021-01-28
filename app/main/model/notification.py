from .. import db, Base
import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy import TIMESTAMP, func
from sqlalchemy_utils import ChoiceType
from app.main.model.subscription import Subscription
from flask import abort
import enum

class Notification(db.Model):
    __tablename__ = 'notification'

    IN_PROGRESS='in_progress'
    DELIVERED='delivered'
    CANCELLED='cancelled'

    DELIVERY_STATUS_TYPES = [
        (IN_PROGRESS,'in_progress'),
        (DELIVERED,'delivered'),
        (CANCELLED,'cancelled')
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    message = db.Column(db.String(150), unique=False, nullable=False)
    created_date = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    last_update = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), server_onupdate=func.now())
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    delivery_status = db.Column(ChoiceType(DELIVERY_STATUS_TYPES), nullable=False, default=IN_PROGRESS)

    @validates('subscription_id')
    def validate_subscription_id(self, key, id):
        if Subscription.query.get(id) == None:
            abort(422)
        return id

