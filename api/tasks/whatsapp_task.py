import logging
from uuid import UUID

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
        app_model = db.session.query(App).filter(App.id == UUID("2813cc15-8da8-4911-8a91-5178f4028f79")).first()
        response = CompletionService.completion(
            app_model=app_model,
            user=end_user,
            args=data,
            invoke_from=InvokeFrom.WEB_APP,
            streaming=False
        )
        token = "EAAFJMpu0YYYBOZBUDAD9Vf9hZCZB6YsZAv8GFNZBi9mrLl0uvWn6Aank4JUnAQKWxDVC4uGMwq1YupzgQZBKTeMvX8lxTnwnHVBZBdZAmXXSLjDRe1RBje4ZA77TOWd6ZAD17o2oOW6LEGPxqQvz9ZAket0SwJerKlRjPCQuYxAKiIpU8sgSsiXMyOdkKZAzFIO35LQAhFmHVHtmA3jQvZBIBJZCdzuqacDrbXVfXKptAZD"
        whatsapp_app = whatsapp_service(phone_number_id="159045903960749", bearer_token=token)
        response = compact_response(response)
        response_data = response.json()
        # Assuming the API returns the message in a key called 'message' - adjust as needed
        message_text = response_data.get("answer", "No answer found.")
        # Use the WhatsApp class to send the fetched message text
        whatsapp_response = whatsapp_app.send_text_message(to=sender_id, message=message_text)
        if whatsapp_response.status != 200:
            logging.error(f"[Whatsapp] Send message error. Status: {whatsapp_response.status}\nError detail: {whatsapp_response.text}")
        else:
            logging.info("[Whatsapp] Message sent successfully.")
    except Exception as error:
        logging.error(f"[Whatsapp] Send message error: {error}")
