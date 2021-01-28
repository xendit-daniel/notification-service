
from flask_restx import Api
from flask import Blueprint
from app.main.controller.subscription_controller import api as subscription_ns
from app.main.controller.notification_controller import api as notification_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Xendit Trial Day Notifcation Service',
          version='1.0',
          description='a web service for sending notifications to specified urls.'
          )

api.add_namespace(subscription_ns, path='/subscription')
api.add_namespace(notification_ns, path='/notification')

