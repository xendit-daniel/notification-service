from app.main.model.subscription import Subscription
from app.main.schema.subscription_schema import SubscriptionBaseSchema
from app.main import db
from typing import Dict, Tuple

def save_new_subscription(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    new_subscription = SubscriptionBaseSchema().load(data=data)
    db.session.add(new_subscription)
    db.session.commit()
    return SubscriptionBaseSchema().dump(new_subscription), 201