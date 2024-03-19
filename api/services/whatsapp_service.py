from whatsapp_cloud_api.whatsappcloudapi import WhatsApp


class WhatsAppService(WhatsApp):
    def __init__(self, phone_number_id: str, bearer_token: str, version: str = "v18.0"):
        self.phone_number_id: str = phone_number_id
        self.bearer_token: str = bearer_token
        self.version: str = version
    
    def __str__(self):
        return f"WhatsApp {self.phone_number_id} {self.version}"

    def __repr__(self):
        return f"WhatsApp {self.phone_number_id} {self.version}"

whatsapp_service = WhatsAppService
