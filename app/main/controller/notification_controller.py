from flask import request, abort
from flask_restx import Resource, Namespace
from app.main.schema.notification_schema import NotificationBaseSchema

from app.main.service.notification_helper import save_new_notification, get_a_notification, update_notification_status

api = Namespace('notification', description='notification related operations')

@api.route('/')
class NotificationList(Resource):
    def post(self):
        post_data = request.json
        return save_new_notification(post_data)

@api.route('/<id>')
class Notification(Resource):
    def get(self, id):
        notification = get_a_notification(id)
        if not notification:
            abort(404)
        else:
            return NotificationBaseSchema().dump(notification), 200
    def patch(self, id):
        notification = get_a_notification(id)
        patch_data = request.json
        if not notification:
            abort(404)
        else:
            return update_notification_status(patch_data, notification)

