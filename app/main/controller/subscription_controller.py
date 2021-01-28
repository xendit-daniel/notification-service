from flask import request, abort
from flask_restx import Resource, Namespace

from app.main.service.subscription_helper import save_new_subscription, get_all_subscriptions, \
    get_a_subscription, update_subscription
from app.main.schema.subscription_schema import SubscriptionBaseSchema

api = Namespace('subscription', description='subscription related operations')

@api.route('/')
class SubscriptionList(Resource):

    def post(self):
        post_data = request.json
        return save_new_subscription(post_data)

    def get(self):
        """List all subscriptions"""
        return get_all_subscriptions()

@api.route('/<id>')
class Subscription(Resource):

    def get(self, id):
        subscription = get_a_subscription(id)
        if not subscription:
            abort(404)
        else:
            return SubscriptionBaseSchema().dump(subscription), 200

    def patch(self, id):
        subscription = get_a_subscription(id)
        patch_data = request.json
        if not subscription:
            abort(404)
        else:
            return update_subscription(patch_data, subscription)
