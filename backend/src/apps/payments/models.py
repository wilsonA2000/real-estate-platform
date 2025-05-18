from django.db import models
from django.contrib.auth import get_user_model
from apps.contracts.models import Contract

User = get_user_model()


class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
    )

    def __str__(self):
        return f"Payment of {self.amount} by {self.payer} for {self.contract}"
