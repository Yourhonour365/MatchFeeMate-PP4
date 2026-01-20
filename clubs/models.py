from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    home_ground = models.CharField(max_length=100, blank=True)
    default_match_fee = models.DecimalField(
        max_digits=5, decimal_places=2, default=10.00
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='clubs_created'
    )

    def __str__(self):
        return self.name