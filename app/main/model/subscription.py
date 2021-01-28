from .. import db
import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, func

class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    subscription_key = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    callback_url = db.Column(URLType, unique=True, nullable=False)
    created_date = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    last_update = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), server_onupdate=func.now())
    notifications = relationship('Notification')