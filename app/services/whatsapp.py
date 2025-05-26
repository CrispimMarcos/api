import requests
from app.core.config import settings
"""
Função para enviar mensagens via WhatsApp usando a API Ultramsg, para enviar mensagem basta chamar esssa função em qualquer lugar do projeto.
"""

def send_whatsapp_message(to: str, message: str):
    url = f"{settings.WHATSAPP_BASE_URL}/{settings.WHATSAPP_INSTANCE_ID}/messages/chat"
    
    payload = {
        "token": settings.WHATSAPP_API_TOKEN,
        "to": to,
        "body": message
    }

    response = requests.post(url, data=payload)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao enviar WhatsApp: {response.text}")
    
    return response.json()
