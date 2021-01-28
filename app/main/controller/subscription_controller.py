from flask import request
from flask_restx import Resource, Namespace

from app.main.service.subscription_helper import save_new_subscription

api = Namespace('subscription', description='subscription related operations')

@api.route('/')
class SubscriptionList(Resource):
    def post(self):
        post_data = request.json
        return save_new_subscription(post_data)
