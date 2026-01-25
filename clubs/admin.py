from django.contrib import admin
from .models import Club, Player, Opposition, Match, MatchPlayer

admin.site.register(Club)
admin.site.register(Player)
admin.site.register(Opposition)
admin.site.register(Match)
admin.site.register(MatchPlayer)