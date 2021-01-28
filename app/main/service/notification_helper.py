from app.main.model.notification import Notification
from app.main.model.subscription import Subscription
from app.main.schema.notification_schema import NotificationBaseSchema, NotificationStatusSchema
from app.main import db
from worker import q
from typing import Dict, Tuple
from rq import Retry
import requests
from app.main import create_app

def send_notification(notification, subscription):
    headers = {'x-api-key': subscription.subscription_key}

    response = requests.post(
    subscription.callback_url, 
    data = {
        'public_id': notification.public_id,
        'title': notification.title,
        'message': notification.message,
        'created_date': notification.created_date,
    })
    
    if response.status_code >= 100 and response.status_code <= 399:
        # status code success: end job
        notification.delivery_status = Notification.DELIVERED
        db.session.add(notification)
        db.session.commit()
    elif 400 <= response.status_code < 500:
        # status code 400: end job
        notification.delivery_status = Notification.CANCELLED
        db.session.add(notification)
        db.session.commit()
    elif 500 <= response.status_code < 600:
        # status code 500: implement exponential backoff
        notification.delivery_status = Notification.CANCELLED
        db.session.add(notification)
        db.session.commit()
        response.raise_for_status()
    

def push_notification(notification):
    if notification.delivery_status == Notification.IN_PROGRESS:
        subscription = Subscription.query.get(notification.subscription_id)
        if subscription.active:
            job = q.enqueue_call(
                send_notification, 
                args=(notification, subscription), 
                result_ttl=500,
                retry=Retry(max=7, interval=[1, 2, 4, 8, 16, 32, 64]),
                timeout='30s',
                failure_ttl=300
            )
        else:
            notification.delivery_status = Notification.CANCELLED
            db.session.add(notification)
            db.session.commit()

def save_new_notification(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    new_notification = NotificationBaseSchema().load(data=data)
    db.session.add(new_notification)
    db.session.commit()
    return NotificationBaseSchema().dump(new_notification), 201

def get_a_notification(id: int) -> Dict[str, str]:
    notification = Notification.query.get(id)
    return notification

def update_notification_status(data: Dict[str, str], notification: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    NotificationStatusSchema().load(data)
    for key in data:
        value = data[key]
        setattr(notification, key, value)
    db.session.commit()
    updated = NotificationBaseSchema().dump(notification)
    push_notification(notification)
    return updated, 200