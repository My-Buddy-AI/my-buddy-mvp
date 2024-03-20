from flask import Response, request, jsonify
import logging
from flask_login import current_user
from flask_restful import Resource, reqparse
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound

from controllers.web import api

from extensions.ext_database import db
from libs.login import login_required
from services.whatsapp_service import whatsapp_service
from core.entities.application_entities import InvokeFrom
from controllers.web.completion import compact_response, CompletionService
from tasks.whatsapp_task import send_whatsapp_response


class WhatasappWebhookApi(Resource):
    def get(self, *args):
        # Log the request query parameters
        parser = reqparse.RequestParser()
        parser.add_argument('hub.challenge', type=str, required=True, location='args')
        args = parser.parse_args()
        return Response(args["hub.challenge"], mimetype='plain/text')

    def post(self):
        body = request.json
        logging.info(f"Wabhook message: {body}")
        if messages := body.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('messages'):
            for message in messages:
                if message.get('type') != 'text':
                    continue

                sender_id = message.get('from')
                msg = message.get('text', {}).get('body', "")

                data = {}
                data["inputs"] = {}
                data["query"] = msg
                data["files"] = [
                    {
                        "type": "image",
                        "transfer_method": "remote_url",
                        "url": "https://my-buddy.ai/wp-content/uploads/2024/01/dark-logo.png",
                    }
                ]
                data["response_mode"] = "blocking"
                data["conversation_id"] = ""
                data["user"] = f"whatsapp-{sender_id}"
                data['auto_generate_name'] = False
        else:
            return jsonify('No messages found'), 200
        send_whatsapp_response.apply_async(kwargs={"data": data, "end_user": None, "sender_id": sender_id})
        return {'result': 'success'}


api.add_resource(WhatasappWebhookApi, '/whatsapp/webhooks')
