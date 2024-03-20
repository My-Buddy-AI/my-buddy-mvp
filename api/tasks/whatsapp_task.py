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
        end_user = create_or_update_end_user_for_user_id(app_model, uuid4())
        response = CompletionService.completion(
            app_model=app_model,
            user=end_user,
            args=data,
            invoke_from=InvokeFrom.WEB_APP,
            streaming=False
        )
        token = "EAAFJMpu0YYYBO4Hd5Amc2dHSCSqQfBHuZCBiQlMZA15mxl2ZAQ97FbuYseuZAUUe4RUrCKgy29kPE84ZCZBRkqltmZCF2Dc0XTFkUIzZAVC61XvdQDSx5VyabZBfKSCSpAYsylmtUq8LZC67CczI0ZAGoVs7Pa2iRsQlVC7BD8UOXTAkp2zNzDM5NP6HMzi8xZBqWngMikqIl0481ODHfQbnqxf1W6eLla66cuiI8wwZD"
        whatsapp_app = whatsapp_service(phone_number_id="159045903960749", bearer_token=token)
        response = compact_response(response)
        logging.info(f"Compact response: {response}")
        response_data = response.json()
        # Assuming the API returns the message in a key called 'message' - adjust as needed
        message_text = response_data.get("answer", "No answer found.")
        logging.info(f"Message for whatsapp: {message_text}")
        # Use the WhatsApp class to send the fetched message text
        whatsapp_response = whatsapp_app.send_text_message(to=sender_id, message=message_text)
        if whatsapp_response.status != 200:
            logging.error(f"[Whatsapp] Send message error. Status: {whatsapp_response.status}\nError detail: {whatsapp_response.text}")
        else:
            logging.info("[Whatsapp] Message sent successfully.")
    except Exception as error:
        logging.error(f"[Whatsapp] Send message error: {error}")
