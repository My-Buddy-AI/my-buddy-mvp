import ast
import logging
from uuid import UUID, uuid4

from controllers.service_api.app import create_or_update_end_user_for_user_id
from services.whatsapp_service import whatsapp_service
from core.entities.application_entities import InvokeFrom
from controllers.web.completion import compact_response, CompletionService
from celery import shared_task
from extensions.ext_database import db
from models.model import App


@shared_task(queue='whatsapp')
def send_whatsapp_response(data: dict, end_user, sender_id):
    try:
        # Get app model
        app_model = db.session.query(App).filter(App.id == "2813cc15-8da8-4911-8a91-5178f4028f79").first()
        end_user = create_or_update_end_user_for_user_id(app_model, str(uuid4()))
        response = CompletionService.completion(
            app_model=app_model,
            user=end_user,
            args=data,
            invoke_from=InvokeFrom.WEB_APP,
            streaming=True
        )
        token = "EAAuaw3HgfGwBO8lHi4S9pgkO6ObkC7XaHMLGe3OnDmJQmvllDbyXVhbcZCRpOEZAN2U0Ch8yYbofPNfPcI0jQohxw0T8uyqvIzZCT89YJEMPZCg6XJjc9CaJi2FuZCgK1VC0hV5tao4SlLnpdNfZC3MZB2kLMFM8qfGzJmnhNl6fYZBx2Hx2On42DWR6Pm2CiPJ4n5JY8frr6mlIsKUpKtSmDEMAeJrLTt15KQZDZD"
        whatsapp_app = whatsapp_service(phone_number_id="280222135167594", bearer_token=token, version='v18.0')
        response = compact_response(response)
        answer = ""
        for x in response.response:
            if len(answer) >= 1550:
                logging.info(f"Message for whatsapp: {answer}")
                # Use the WhatsApp class to send the fetched message text
                whatsapp_response = whatsapp_app.send_text_message(to=sender_id, message=answer)
                if whatsapp_response.status_code != 200:
                    logging.error(f"[Whatsapp] Send message error. Status: {whatsapp_response.status_code}\nError detail: {whatsapp_response.text}")
                else:
                    logging.info("[Whatsapp] Message sent successfully.")
                answer = ""
            answer += f" {ast.literal_eval(x[6:]).get('answer', '')}"
        else:
            logging.info(f"Message for whatsapp: {answer}")
            # Use the WhatsApp class to send the fetched message text
            whatsapp_response = whatsapp_app.send_text_message(to=sender_id, message=answer)
            if whatsapp_response.status_code != 200:
                logging.error(f"[Whatsapp] Send message error. Status: {whatsapp_response.status_code}\nError detail: {whatsapp_response.text}")
            else:
                logging.info("[Whatsapp] Message sent successfully.")
    except Exception as error:
        logging.error(f"[Whatsapp] Send message error: {error}")
