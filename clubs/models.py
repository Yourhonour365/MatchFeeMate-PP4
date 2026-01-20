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

class Player(models.Model):
    """A player/member belonging to a club"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('captain', 'Captain'),
        ('player', 'Player'),
    ]
    
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name='players'
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='player_profiles'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.club.name})"
    
class Opposition(models.Model):
    """Opposition teams that the club plays against"""
    
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name='oppositions'
    )
    name = models.CharField(max_length=100)
    home_ground = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name