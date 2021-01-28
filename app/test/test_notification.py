import unittest
# from mock import patch, Mock
from app.main import db
from app.main.model.notification import Notification
from app.main.model.subscription import Subscription
import json
from app.test.base import BaseTestCase

class TestNotification(BaseTestCase):
    # POST
    def test_create_notification(self):
        """Test for notification creation"""
        with self.client:
            subscription = Subscription(
                customer_id=1,
                callback_url="http://0.0.0.0:80/post",
            )
            db.session.add(subscription)
            db.session.commit()
            response = self.client.post(
                '/notification/',
                data=json.dumps(dict(
                    message="Sample Message",
                    title="Sample Title",
                    subscription_id=subscription.id
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Sample Message")
            self.assertTrue(data['title'] == "Sample Title")
            self.assertTrue(data['subscription_id'] == subscription.id)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_create_notification_no_subscription_id(self):
        """Test for notification creation"""
        with self.client:
            response = self.client.post(
                '/notification/',
                data=json.dumps(dict(
                    message="Sample Message",
                    title="Sample Title",
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['subscription_id'] == ['Missing data for required field.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_create_notification_subscriber_not_exist(self):
        """Test for notification creation"""
        with self.client:
            response = self.client.post(
                '/notification/',
                data=json.dumps(dict(
                    message="Sample Message",
                    title="Sample Title",
                    subscription_id=1
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    def test_create_notification_no_message(self):
        """Test for notification creation"""
        with self.client:
            subscription = Subscription(
                customer_id=1,
                callback_url="http://0.0.0.0:80/post",
            )
            db.session.add(subscription)
            db.session.commit()
            response = self.client.post(
                '/notification/',
                data=json.dumps(dict(
                    title="Sample Title",
                    subscription_id=subscription.id
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == ['Missing data for required field.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_create_notification_no_title(self):
        """Test for notification creation"""
        with self.client:
            subscription = Subscription(
                customer_id=1,
                callback_url="http://0.0.0.0:80/post",
            )
            db.session.add(subscription)
            db.session.commit()
            response = self.client.post(
                '/notification/',
                data=json.dumps(dict(
                    message="Sample Message",
                    subscription_id=subscription.id
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['title'] == ['Missing data for required field.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_get_notifications(self):
        subscription = Subscription(
                customer_id=1,
                callback_url="http://0.0.0.0:80/post",
        )
        db.session.add(subscription)
        db.session.commit()
        notification = Notification(
            message="Sample Message",
            subscription_id=subscription.id,
            title="Sample Title"
        )
        db.session.add(notification)
        db.session.commit()
        with self.client:
            response = self.client.get(
                '/notification/',
            )
            
            data = json.loads(response.data.decode())
            self.assertEqual(len(data), 1)
            self.assertTrue(data[0]['message'] == "Sample Message")
            self.assertTrue(data[0]['subscription_id'] == subscription.id)
            self.assertTrue(data[0]['title'] == "Sample Title")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    
    def test_get_notifications(self):
        subscription = Subscription(
                customer_id=1,
                callback_url="http://0.0.0.0:80/post",
        )
        db.session.add(subscription)
        db.session.commit()
        notification = Notification(
            message="Sample Message",
            subscription_id=subscription.id,
            title="Sample Title"
        )
        db.session.add(notification)
        db.session.commit()
        with self.client:
            response = self.client.get(
                '/notification/{}'.format(str(notification.id)),
            )
            
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == "Sample Message")
            self.assertTrue(data['subscription_id'] == subscription.id)
            self.assertTrue(data['title'] == "Sample Title")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    
    def test_get_notifications(self):
        with self.client:
            response = self.client.get(
                '/notification/1',
            )
            
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)
    
    def test_patch_notification_status(self):
        """Test for notification update"""
        subscription = Subscription(
                customer_id=1,
                callback_url="http://0.0.0.0:80/post",
        )
        db.session.add(subscription)
        db.session.commit()
        notification = Notification(
            message="Sample Message",
            subscription_id=subscription.id,
            title="Sample Title"
        )
        db.session.add(notification)
        db.session.commit()
        with self.client:
            response = self.client.patch(
                '/notification/{}'.format(notification.id),
                data=json.dumps(dict(
                    delivery_status='cancelled',
                )),
                content_type='application/json'
            )
            
            data = json.loads(response.data.decode())
            self.assertTrue(data['delivery_status'] == 'cancelled')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    


if __name__ == '__main__':
    unittest.main()