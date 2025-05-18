from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Relationship(models.Model):
    user1 = models.ForeignKey(
        User, related_name="relationships_as_user1", on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, related_name="relationships_as_user2", on_delete=models.CASCADE
    )
    relationship_type = models.CharField(
        max_length=50,
        choices=[
            ("arrendador-arrendatario", "Arrendador-Arrendatario"),
            ("arrendatario-prestador", "Arrendatario-Prestador"),
            ("arrendador-prestador", "Arrendador-Prestador"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2", "relationship_type")


class Rating(models.Model):
    from_user = models.ForeignKey(
        User, related_name="given_ratings", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="received_ratings", on_delete=models.CASCADE
    )
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
