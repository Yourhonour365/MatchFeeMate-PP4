from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Club, Player, Opposition, Match, MatchPlayer
from .forms import ClubForm, PlayerForm, OppositionForm, MatchForm
from django.core.exceptions import PermissionDenied


def home(request):
    """Display the homepage - redirect to club if user has one"""
    if request.user.is_authenticated:
        # Check if user has a club (as a player)
        player = Player.objects.filter(user=request.user).first()
        if player:
            return redirect('club_detail', pk=player.club.pk)
    return render(request, 'clubs/home.html')

@login_required
def club_create(request):
    """Create a new club - only logged in users can access"""
    if request.method == 'POST':
        # Form was submitted
        form = ClubForm(request.POST)
        if form.is_valid():
            # Save but don't commit yet - we need to add the user
            club = form.save(commit=False)
            club.created_by = request.user
            club.save()
            # Create the user as admin of this club
            Player.objects.create(
                club=club,
                user=request.user,
                name=request.user.email,
                email=request.user.email,
                role='admin'
            )
            return redirect('club_detail', pk=club.pk)
    else:
        # Show empty form
        form = ClubForm()
    return render(request, 'clubs/club_form.html', {'form': form})


@login_required
def club_detail(request, pk):
    """View a single club's details"""
    club = get_object_or_404(Club, pk=pk)
    return render(request, 'clubs/club_detail.html', {'club': club})


@login_required
def club_update(request, pk):
    """Edit an existing club"""
    club = get_object_or_404(Club, pk=pk)
    # Permission check - only admin/captain can edit club
    if not club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        # Form was submitted with changes
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect('club_detail', pk=club.pk)
    else:
        # Show form pre-filled with current data
        form = ClubForm(instance=club)
    return render(request, 'clubs/club_form.html', {'form': form, 'club': club})


@login_required
def club_delete(request, pk):
    """Delete a club - requires POST confirmation"""
    club = get_object_or_404(Club, pk=pk)
    # Permission check - only admin/captain can delete club
    if not club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        club.delete()
        return redirect('home')
    return render(request, 'clubs/club_confirm_delete.html', {'club': club})

@login_required
def player_create(request, club_pk):
    """Create a new player for a specific club"""
    club = get_object_or_404(Club, pk=club_pk)
    # Permission check - only admin/captain can add players
    if not club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.club = club
            player.save()
            return redirect('club_detail', pk=club.pk)
    else:
        form = PlayerForm()
    return render(request, 'clubs/player_form.html', {'form': form, 'club': club})


@login_required
def player_update(request, pk):
    """Edit an existing player"""
    player = get_object_or_404(Player, pk=pk)
    # Permission check - only admin/captain can edit players
    if not player.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('club_detail', pk=player.club.pk)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'clubs/player_form.html', {'form': form, 'player': player, 'club': player.club})


@login_required
def player_delete(request, pk):
    """Delete a player - requires POST confirmation"""
    player = get_object_or_404(Player, pk=pk)
    # Permission check - only admin/captain can delete players
    if not player.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    club_pk = player.club.pk
    if request.method == 'POST':
        player.delete()
        return redirect('club_detail', pk=club_pk)
    return render(request, 'clubs/player_confirm_delete.html', {'player': player})

@login_required
def opposition_create(request, club_pk):
    """Create a new opposition team for a specific club"""
    club = get_object_or_404(Club, pk=club_pk)
    # Permission check - only admin/captain can add opposition
    if not club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = OppositionForm(request.POST)
        if form.is_valid():
            opposition = form.save(commit=False)
            opposition.club = club
            opposition.save()
            return redirect('club_detail', pk=club.pk)
    else:
        form = OppositionForm()
    return render(request, 'clubs/opposition_form.html', {'form': form, 'club': club})


@login_required
def opposition_update(request, pk):
    """Edit an existing opposition team"""
    opposition = get_object_or_404(Opposition, pk=pk)
    # Permission check - only admin/captain can edit opposition
    if not opposition.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = OppositionForm(request.POST, instance=opposition)
        if form.is_valid():
            form.save()
            return redirect('club_detail', pk=opposition.club.pk)
    else:
        form = OppositionForm(instance=opposition)
    return render(request, 'clubs/opposition_form.html', {'form': form, 'opposition': opposition, 'club': opposition.club})


@login_required
def opposition_delete(request, pk):
    """Delete an opposition team"""
    opposition = get_object_or_404(Opposition, pk=pk)
    # Permission check - only admin/captain can delete opposition
    if not opposition.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    club_pk = opposition.club.pk
    if request.method == 'POST':
        opposition.delete()
        return redirect('club_detail', pk=club_pk)
    return render(request, 'clubs/opposition_confirm_delete.html', {'opposition': opposition})


@login_required
def match_create(request, club_pk):
    """Create a new match for a specific club"""
    club = get_object_or_404(Club, pk=club_pk)
    # Permission check - only admin/captain can add matches
    if not club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.club = club
            # Auto-fill venue if empty
            if not match.venue or not match.venue.strip():
                if match.is_home:
                    match.venue = club.home_ground
                else:
                    match.venue = match.opposition.home_ground
            match.save()
            return redirect('match_detail', pk=match.pk)
    else:
        form = MatchForm(initial={'match_fee': club.default_match_fee, 'time': '13:00'})
        # Only show opposition teams for this club
        form.fields['opposition'].queryset = Opposition.objects.filter(club=club)
    return render(request, 'clubs/match_form.html', {'form': form, 'club': club})


@login_required
def match_detail(request, pk):
    """View a single match's details"""
    match = get_object_or_404(Match, pk=pk)
    
    # Count selected and available
    match_players = match.match_players.all()
    selected_count = match_players.filter(selected=True).count()
    available_count = match_players.filter(availability='yes', selected=False).count()
    
    # Warning: selected but not available
    unavailable_selected = match_players.filter(selected=True).exclude(availability='yes')
    
    return render(request, 'clubs/match_detail.html', {
        'match': match,
        'selected_count': selected_count,
        'available_count': available_count,
        'unavailable_selected': unavailable_selected,
    })


@login_required
def match_update(request, pk):
    """Edit an existing match"""
    match = get_object_or_404(Match, pk=pk)
    # Permission check - only admin/captain can edit matches
    if not match.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('match_detail', pk=match.pk)
    else:
        form = MatchForm(instance=match)
        # Only show opposition teams for this club
        form.fields['opposition'].queryset = Opposition.objects.filter(club=match.club)
    return render(request, 'clubs/match_form.html', {'form': form, 'match': match, 'club': match.club})


@login_required
def match_delete(request, pk):
    """Delete a match"""
    match = get_object_or_404(Match, pk=pk)
    # Permission check - only admin/captain can delete matches
    if not match.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    club_pk = match.club.pk
    if request.method == 'POST':
        match.delete()
        return redirect('club_detail', pk=club_pk)
    return render(request, 'clubs/match_confirm_delete.html', {'match': match})

@login_required
def set_availability(request, match_pk, availability):
    """Set player's availability for a match"""
    match = get_object_or_404(Match, pk=match_pk)
    # Find player record for this user in this club
    player = Player.objects.filter(club=match.club, user=request.user).first()
    if not player:
        raise PermissionDenied
    
    # Create or update availability
    match_player, created = MatchPlayer.objects.get_or_create(
        match=match,
        player=player,
        defaults={'availability': availability}
    )
    if not created:
        match_player.availability = availability
        match_player.save()
    
    return redirect('match_detail', pk=match_pk)

@login_required
def team_selection(request, match_pk):
    """Captain selects players for the match"""
    match = get_object_or_404(Match, pk=match_pk)
    # Permission check - only admin/captain can select team
    if not match.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    
    # Get all players and their availability for this match
    players = Player.objects.filter(club=match.club, is_active=True)
    
    # Split players into categories
    selected_players = []
    available_players = []
    maybe_players = []
    unavailable_players = []
    
    for player in players:
        mp = match.match_players.filter(player=player).first()
        player.is_selected = mp.selected if mp else False
        player.availability = mp.availability if mp else 'maybe'
        
        if player.is_selected:
            selected_players.append(player)
        elif player.availability == 'yes':
            available_players.append(player)
        elif player.availability == 'maybe':
            maybe_players.append(player)
        else:
            unavailable_players.append(player)
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected')
        # Update all match_players for this match
        for player in players:
            match_player, created = MatchPlayer.objects.get_or_create(
                match=match,
                player=player,
                defaults={'availability': 'maybe'}
            )
            match_player.selected = str(player.pk) in selected_ids
            match_player.save()
        return redirect('match_detail', pk=match_pk)
    
    return render(request, 'clubs/team_selection.html', {
        'match': match,
        'selected_players': selected_players,
        'available_players': available_players,
        'maybe_players': maybe_players,
        'unavailable_players': unavailable_players,
    })

@login_required
def bulk_availability(request, match_pk):
    """Admin updates multiple players' availability at once"""
    match = get_object_or_404(Match, pk=match_pk)
    # Permission check - only admin/captain can update availability
    if not match.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    
    players = Player.objects.filter(club=match.club, is_active=True)
    
    # Split players into selected and other
    selected_players = []
    other_players = []
    
    for player in players:
        mp = match.match_players.filter(player=player).first()
        player.current_availability = mp.get_availability_display() if mp else 'Awaiting response'
        player.is_selected = mp.selected if mp else False
        
        if player.is_selected:
            selected_players.append(player)
        else:
            other_players.append(player)
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('players')
        new_availability = request.POST.get('availability')
        
        for player_id in selected_ids:
            player = Player.objects.get(pk=player_id)
            match_player, created = MatchPlayer.objects.get_or_create(
                match=match,
                player=player,
                defaults={'availability': new_availability}
            )
            if not created:
                match_player.availability = new_availability
                match_player.save()
        
        return redirect('match_detail', pk=match_pk)
    
    return render(request, 'clubs/bulk_availability.html', {
        'match': match,
        'selected_players': selected_players,
        'other_players': other_players,
    })

@login_required
def match_list(request):
    """List all matches for user's club"""
    player = Player.objects.filter(user=request.user).first()
    if not player:
        return redirect('home')
    
    matches = Match.objects.filter(club=player.club).order_by('date')
    return render(request, 'clubs/match_list.html', {
        'matches': matches,
        'club': player.club,
    })


@login_required
def player_list(request):
    """List all players for user's club"""
    player = Player.objects.filter(user=request.user).first()
    if not player:
        return redirect('home')
    
    players = Player.objects.filter(club=player.club, is_active=True)
    return render(request, 'clubs/player_list.html', {
        'players': players,
        'club': player.club,
    })