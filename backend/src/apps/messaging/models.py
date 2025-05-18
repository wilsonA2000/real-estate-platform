from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    contract = models.ForeignKey(
        "real_estate_auth.Contract",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )  # Uso de string para evitar importación circular
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_recipient = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}: {self.subject}"
