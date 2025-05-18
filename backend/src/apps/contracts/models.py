from django.db import models
from django.contrib.auth import get_user_model
from apps.properties.models import Property

User = get_user_model()


class Contract(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contracts_bought"
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contracts_sold"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
    )

    def __str__(self):
        return f"Contract for {self.property} between {self.buyer} and {self.seller}"
