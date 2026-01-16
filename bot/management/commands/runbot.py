from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot.models import TelegramUser
from django.conf import settings
from asgiref.sync import sync_to_async  # Needed for async-safe ORM

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.from_user
    chat_id = update.message.chat.id

    # Async-safe ORM call
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        telegram_id=str(chat_id),
        defaults={
            "username": user_data.username,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
        }
    )

    if created:
        await update.message.reply_text(f"Hi {user.first_name}, you are now subscribed!")
    else:
        await update.message.reply_text(f"Hi {user.first_name}, you are already subscribed!")

class Command(BaseCommand):
    help = "Run Telegram bot (polling, v20+)"

    def handle(self, *args, **kwargs):
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))

        print("Bot is running (polling)... Users who click /start will be stored.")
        app.run_polling()
