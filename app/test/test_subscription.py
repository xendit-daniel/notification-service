import unittest
# from mock import patch, Mock
from app.main import db
from app.main.model.subscription import Subscription
import json
from app.test.base import BaseTestCase

class TestSubscription(BaseTestCase):
    # POST
    def test_create_subscription(self):
        """Test for subscription creation"""
        with self.client:
            response = self.client.post(
                '/subscription/',
                data=json.dumps(dict(
                    customer_id=1,
                    callback_url="http://0.0.0.0:80/random"
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['customer_id'] == 1)
            self.assertTrue(data['callback_url'] == 'http://0.0.0.0:80/random')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_create_subscription_no_customer_id(self):
        """Test for subscription creation"""
        with self.client:
            response = self.client.post(
                '/subscription/',
                data=json.dumps(dict(
                    callback_url="http://0.0.0.0:80/random"
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['customer_id'] == ['Missing data for required field.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_create_subscription_no_url(self):
        """Test for subscription creation"""
        with self.client:
            response = self.client.post(
                '/subscription/',
                data=json.dumps(dict(
                    customer_id=1,
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['callback_url'] == ['Missing data for required field.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_create_subscription_no_payload(self):
        """Test for subscription creation"""
        with self.client:
            response = self.client.post(
                '/subscription/',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['customer_id'] == ['Missing data for required field.'])
            self.assertTrue(data['callback_url'] == ['Missing data for required field.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_create_subscription_invalid_customer_id(self):
        """Test for subscription creation"""
        with self.client:
            response = self.client.post(
                '/subscription/',
                data=json.dumps(dict(
                    customer_id="Some_invalid_input",
                    callback_url="http://0.0.0.0:80/random"
                )),
                content_type='application/json'
            )
            
            data = json.loads(response.data.decode())
            self.assertTrue(data['customer_id'] == ['Not a valid integer.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
    
    def test_create_subscription_invalid_url(self):
        """Test for subscription creation"""
        with self.client:
            response = self.client.post(
                '/subscription/',
                data=json.dumps(dict(
                    customer_id=1,
                    callback_url="invalid_url_string"
                )),
                content_type='application/json'
            )
            
            data = json.loads(response.data.decode())
            self.assertTrue(data['callback_url'] == ['Not a valid URL.'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_get_subscriptions(self):
        subscription = Subscription(
            customer_id=1,
            callback_url="http://0.0.0.0:80/post",
        )
        db.session.add(subscription)
        db.session.commit()
        with self.client:
            response = self.client.get(
                '/subscription/',
            )
            
            data = json.loads(response.data.decode())
            self.assertEqual(len(data), 1)
            self.assertTrue(data[0]['callback_url'] == "http://0.0.0.0:80/post")
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data[0]['customer_id'] == 1)
            self.assertEqual(response.status_code, 200)
    
    def test_get_subscription(self):
        subscription = Subscription(
            customer_id=1,
            callback_url="http://0.0.0.0:80/post",
        )
        db.session.add(subscription)
        db.session.commit()
        with self.client:
            response = self.client.get(
                '/subscription/1/',
            )
            
            data = json.loads(response.data.decode())
            self.assertTrue(data['callback_url'] == "http://0.0.0.0:80/post")
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['customer_id'] == 1)
            self.assertEqual(response.status_code, 200)
    
    def test_get_subscription_not_found(self):
        subscription = Subscription(
            customer_id=1,
            callback_url="http://0.0.0.0:80/post",
        )
        db.session.add(subscription)
        db.session.commit()
        with self.client:
            response = self.client.get(
                '/subscription/2/',
            )
            self.assertEqual(response.status_code, 404)
    
    def test_patch_subscription_status(self):
        """Test for subscription update"""
        subscription = Subscription(
            customer_id=1,
            callback_url="http://0.0.0.0:80/post",
        )
        db.session.add(subscription)
        db.session.commit()
        with self.client:
            response = self.client.patch(
                '/subscription/1',
                data=json.dumps(dict(
                    active=True,
                )),
                content_type='application/json'
            )
            
            data = json.loads(response.data.decode())
            self.assertTrue(data['active'] == True)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    


if __name__ == '__main__':
    unittest.main()