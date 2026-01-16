from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username or self.first_name} ({self.telegram_id})"


class BotMessage(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user}: {self.message_text[:30]}"
