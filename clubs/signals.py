from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Player

User = get_user_model()

@receiver(post_save, sender=User)
def link_player_to_user(sender, instance, created, **kwargs):
    """When a user signs up, link them to any Player with matching email"""
    if created:
        Player.objects.filter(email=instance.email, user__isnull=True).update(user=instance)