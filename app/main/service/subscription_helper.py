from app.main.model.subscription import Subscription
from app.main.schema.subscription_schema import SubscriptionBaseSchema, SubscriptionUpdateSchema
from app.main import db
from typing import Dict, Tuple

def save_new_subscription(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    new_subscription = SubscriptionBaseSchema().load(data=data)
    db.session.add(new_subscription)
    db.session.commit()
    return SubscriptionBaseSchema().dump(new_subscription), 201

def get_all_subscriptions():
    subscriptions = Subscription.query.all()
    return SubscriptionBaseSchema(many=True).dump(subscriptions), 200

def get_a_subscription(id: int) -> Dict[str, str]:
    subscription = Subscription.query.get(id)
    return subscription

def update_subscription(data: Dict[str, str], subscription: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    SubscriptionUpdateSchema().load(data)
    for key in data:
        value = data[key]
        setattr(subscription, key, value)
    db.session.commit()
    updated = SubscriptionUpdateSchema().dump(subscription)
    return updated, 200