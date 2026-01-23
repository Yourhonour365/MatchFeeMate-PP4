from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Player

User = get_user_model()


@receiver(post_save, sender=User)
def link_user_to_players(sender, instance, created, **kwargs):
    """When user signs up, link to ALL matching unlinked Players"""
    if created and instance.email:
        Player.objects.filter(
            email__iexact=instance.email,
            user__isnull=True
        ).update(user=instance)


@receiver(post_save, sender=Player)
def link_player_to_user(sender, instance, created, **kwargs):
    """When Player created, link to existing User if email matches"""
    if created and instance.email and not instance.user:
        user = User.objects.filter(email__iexact=instance.email).first()
        if user:
            instance.user = user
            instance.save()