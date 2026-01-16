from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from .models import TelegramUser, BotMessage  # Use BotMessage
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

def send_reply(chat_id, text, user=None):
    """Send message to user and track it in DB"""
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": chat_id, "text": text}
    )

    if response.status_code == 200 and user:
        # Save sent message in DB
        BotMessage.objects.create(user=user, message_text=text)

@csrf_exempt
def telegram_webhook(request, token):
    if request.method == "POST" and token == TELEGRAM_TOKEN:
        data = json.loads(request.body)
        message = data.get("message")
        if not message:
            return JsonResponse({"status": "no message"})

        chat_id = message["chat"]["id"]
        telegram_user_id = str(message["from"]["id"])
        username = message["from"].get("username")
        first_name = message["from"].get("first_name")
        last_name = message["from"].get("last_name")
        message_text = message.get("text", "")

        # Save or get user
        user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_user_id,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        # Compose bot reply
        reply_text = f"You said: {message_text}"

        # Send reply and track it
        send_reply(chat_id, reply_text, user=user)

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "invalid"})
