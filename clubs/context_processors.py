from .models import Player

def player_context(request):
    """Add current player to all templates"""
    if request.user.is_authenticated:
        player = Player.objects.filter(user=request.user).first()
        return {'current_player': player}
    return {}