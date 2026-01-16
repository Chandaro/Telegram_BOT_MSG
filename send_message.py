import os
import django
import requests

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytelegram.settings")
django.setup()

from bot.models import TelegramUser, BotMessage
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

def send_message_to_user(chat_id, text, user=None):
    """Send a message and store it in DB if user is provided"""
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": chat_id, "text": text}
    )

    if response.status_code == 200 and user:
        BotMessage.objects.create(user=user, message_text=text)
        print(f"✅ Sent to {user.first_name} ({chat_id})")
    else:
        print(f"❌ Failed to send to chat_id {chat_id}: {response.text}")

def main():
    mode = input("Send to (A)ll users or (S)pecific user? [A/S]: ").strip().upper()
    message_text = input("Type the message to send: ")

    if mode == "A":
        users = TelegramUser.objects.all()
        if not users:
            print("No users found. Ask users to click /start first!")
            return
        for user in users:
            send_message_to_user(user.telegram_id, message_text, user=user)
    elif mode == "S":
        chat_id = input("Enter the chat_id of the user: ").strip()
        try:
            user = TelegramUser.objects.get(telegram_id=chat_id)
            send_message_to_user(chat_id, message_text, user=user)
        except TelegramUser.DoesNotExist:
            print("User with this chat_id not found.")
    else:
        print("Invalid choice. Choose A or S.")

if __name__ == "__main__":
    main()
