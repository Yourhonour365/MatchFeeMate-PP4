from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Club, Player, Opposition, Match, MatchPlayer
from .forms import ClubForm, PlayerForm, OppositionForm, MatchForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse


def home(request):
    """Display the homepage - redirect to club if user has one"""
    if request.user.is_authenticated:
        # Check if user has a club (as a player)
        player = Player.objects.filter(user=request.user).first()
        if player:
            return redirect('match_list')
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
                name=request.POST.get('admin_name'),
                email=request.user.email,
                phone=request.POST.get('admin_phone', ''),
                role='admin'
            )
            messages.success(request, 'Club created successfully.')
            return redirect('club_detail', pk=club.pk)
    else:
        # Show empty form
        form = ClubForm()
    return render(request, 'clubs/club_form.html', {'form': form})


@login_required
def club_detail(request, pk):
    """View a single club's details"""
    club = get_object_or_404(Club, pk=pk)
    is_admin_or_captain = club.is_admin_or_captain(request.user)
    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'is_admin_or_captain': is_admin_or_captain,
    })


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
            messages.success(
                request, 'Club updated successfully.')
            return redirect('club_update', pk=club.pk)
    else:
        # Show form pre-filled with current data
        form = ClubForm(instance=club)
    return render(
        request, 'clubs/club_form.html', {'form': form, 'club': club})


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
            messages.success(request, 'Player added successfully.')
            if 'add_another' in request.POST:
                return redirect('player_create', club_pk=club.pk)
            return redirect('player_availability', player_pk=player.pk)
    else:
        form = PlayerForm()
    return render(
        request, 'clubs/player_form.html', {'form': form, 'club': club})


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
    return render(request, 'clubs/player_form.html', {
        'form': form,
        'player': player,
        'club': player.club
    })


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
    return render(request, 'clubs/player_confirm_delete.html', {
        'player': player
    })


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
            messages.success(request, 'Opposition added successfully.')
            return redirect('opposition_create', club_pk=club.pk)
    else:
        form = OppositionForm()
    return render(request, 'clubs/opposition_form.html', {
        'form': form,
        'club': club
    })


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
            messages.success(request, 'Opposition updated successfully.')
            return redirect('opposition_update', pk=opposition.pk)
    else:
        form = OppositionForm(instance=opposition)
    return render(request, 'clubs/opposition_form.html', {
        'form': form,
        'opposition': opposition,
        'club': opposition.club
    })


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
    return render(request, 'clubs/opposition_confirm_delete.html', {
        'opposition': opposition
    })


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
            new_match = form.save(commit=False)
            new_match.club = club
            # Auto-fill venue if empty
            if not new_match.venue or not new_match.venue.strip():
                if new_match.is_home:
                    new_match.venue = club.home_ground
                else:
                    new_match.venue = new_match.opposition.home_ground
            new_match.save()
            messages.success(request, 'Match created successfully.')
            return redirect('team_selection', match_pk=new_match.pk)
    else:
        form = MatchForm(
            initial={'match_fee': club.default_match_fee, 'time': '13:00'})
        # Only show opposition teams for this club
        form.fields['opposition'].queryset = Opposition.objects.filter(
            club=club)
    return render(request, 'clubs/match_form.html', {
        'form': form,
        'club': club
    })


@login_required
def match_detail(request, pk):
    """View a single match's details"""
    current_match = get_object_or_404(Match, pk=pk)

    # Count selected and available
    match_players = current_match.match_players.all()
    selected_count = match_players.filter(selected=True).count()
    available_count = match_players.filter(
        availability='yes', selected=False).count()

    # Warning: selected but not available
    unavailable_selected = match_players.filter(
        selected=True).exclude(availability='yes')

    # Permission check
    is_admin_or_captain = current_match.club.is_admin_or_captain(request.user)

    # Players who haven't responded yet
    responded_player_ids = match_players.values_list('player_id', flat=True)
    not_responded = Player.objects.filter(
        club=current_match.club, is_active=True
    ).exclude(id__in=responded_player_ids)

    return render(request, 'clubs/match_detail.html', {
        'match': current_match,
        'selected_count': selected_count,
        'available_count': available_count,
        'unavailable_selected': unavailable_selected,
        'is_admin_or_captain': is_admin_or_captain,
        'not_responded': not_responded,
    })


@login_required
def match_update(request, pk):
    """Edit an existing match"""
    current_match = get_object_or_404(Match, pk=pk)
    # Permission check - only admin/captain can edit matches
    if not current_match.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=current_match)
        if form.is_valid():
            form.save()
            messages.success(request, 'Match updated successfully.')
            return redirect('match_update', pk=current_match.pk)
    else:
        form = MatchForm(instance=current_match)
        # Only show opposition teams for this club
        form.fields['opposition'].queryset = Opposition.objects.filter(
            club=current_match.club)
    return render(request, 'clubs/match_form.html', {
        'form': form,
        'match': current_match,
        'club': current_match.club
    })


@login_required
def match_delete(request, pk):
    """Delete a match"""
    current_match = get_object_or_404(Match, pk=pk)
    # Permission check - only admin/captain can delete matches
    if not current_match.club.is_admin_or_captain(request.user):
        raise PermissionDenied
    club_pk = current_match.club.pk
    if request.method == 'POST':
        current_match.delete()
        return redirect('club_detail', pk=club_pk)
    return render(
        request, 'clubs/match_confirm_delete.html', {'match': current_match})


@login_required
def set_availability(request, match_pk, availability):
    """Set player's availability for a match"""
    current_match = get_object_or_404(Match, pk=match_pk)
    # Find player record for this user in this club
    player = Player.objects.filter(
        club=current_match.club, user=request.user).first()
    if not player:
        raise PermissionDenied

    # Create or update availability
    match_player, created = MatchPlayer.objects.get_or_create(
        match=current_match,
        player=player,
        defaults={'availability': availability}
    )
    if not created:
        match_player.availability = availability
        match_player.save()

    # Redirect back to where user came from, or match detail
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('match_detail', pk=match_pk)


@login_required
def team_selection(request, match_pk):
    """Captain selects players for the match"""
    current_match = get_object_or_404(Match, pk=match_pk)
    # Permission check - only admin/captain can select team
    if not current_match.club.is_admin_or_captain(request.user):
        raise PermissionDenied

    # Get current user's player record
    current_player = Player.objects.filter(user=request.user).first()

    # Get all players and their availability for this match
    players = Player.objects.filter(club=current_match.club, is_active=True)

    # Split players into categories
    selected_players = []
    available_players = []
    maybe_players = []
    awaiting_players = []
    unavailable_players = []

    for player in players:
        mp = current_match.match_players.filter(player=player).first()
        player.is_selected = mp.selected if mp else False
        player.availability = mp.availability if mp else None
        player.is_current_user = (player == current_player)

        if player.is_selected:
            selected_players.append(player)
        elif player.availability == 'yes':
            available_players.append(player)
        elif player.availability == 'maybe':
            maybe_players.append(player)
        elif player.availability is None:
            awaiting_players.append(player)
        else:
            unavailable_players.append(player)

    # Sort selected players: available first, then maybe,
    # then awaiting, then unavailable
    def selection_sort_key(p):
        if p.availability == 'yes':
            return (0, p.name.lower())
        elif p.availability == 'maybe':
            return (1, p.name.lower())
        elif p.availability is None:
            return (2, p.name.lower())
        else:
            return (3, p.name.lower())

    selected_players.sort(key=selection_sort_key)

    # Sort other lists alphabetically
    available_players.sort(key=lambda p: p.name.lower())
    maybe_players.sort(key=lambda p: p.name.lower())
    awaiting_players.sort(key=lambda p: p.name.lower())
    unavailable_players.sort(key=lambda p: p.name.lower())

    # Warning: selected but not available
    unavailable_selected = [
        p for p in selected_players if p.availability != 'yes']

    if request.method == 'POST':
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected')
        current_accordion = request.POST.get(
            'current_accordion', 'selectedPlayers')

        if action == 'set_available':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': 'yes'}
                )
                match_player.availability = 'yes'
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) set to Available.')
            return redirect(
                f"{reverse('team_selection', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'set_maybe':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': 'maybe'}
                )
                match_player.availability = 'maybe'
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) set to Maybe.')
            return redirect(
                f"{reverse('team_selection', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'set_unavailable':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': 'no'}
                )
                match_player.availability = 'no'
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) set to Unavailable.')
            return redirect(
                f"{reverse('team_selection', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'add_to_team':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': None}
                )
                match_player.selected = True
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) added to team.')
            return redirect(
                f"{reverse('team_selection', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'remove_from_team':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': None}
                )
                match_player.selected = False
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) removed from team.')
            return redirect(
                f"{reverse('team_selection', args=[match_pk])}"
                f"?open={current_accordion}")

    # Get which accordion to open from URL param
    open_accordion = request.GET.get('open', 'selectedPlayers')

    # Count total available (selected + not selected but available)
    total_available = len(available_players) + len(
        [p for p in selected_players if p.availability == 'yes'])

    return render(request, 'clubs/team_selection.html', {
        'match': current_match,
        'selected_players': selected_players,
        'available_players': available_players,
        'maybe_players': maybe_players,
        'awaiting_players': awaiting_players,
        'unavailable_players': unavailable_players,
        'unavailable_selected': unavailable_selected,
        'open_accordion': open_accordion,
        'total_available': total_available,
    })


@login_required
def bulk_availability(request, match_pk):
    """View/manage availability for all players for a match"""
    current_match = get_object_or_404(Match, pk=match_pk)

    # Permission check - only admin/captain can manage availability
    if not current_match.club.is_admin_or_captain(request.user):
        raise PermissionDenied

    # Get current user's player record
    current_player = Player.objects.filter(user=request.user).first()

    # Get all players and their availability for this match
    players = Player.objects.filter(club=current_match.club, is_active=True)

    # Split players into categories by availability only (not selection)
    available_players = []
    maybe_players = []
    awaiting_players = []
    unavailable_players = []
    selected_count = 0

    for player in players:
        mp = current_match.match_players.filter(player=player).first()
        player.is_selected = mp.selected if mp else False
        player.availability = mp.availability if mp else None
        player.is_current_user = (player == current_player)

        if player.is_selected:
            selected_count += 1

        if player.availability == 'yes':
            available_players.append(player)
        elif player.availability == 'maybe':
            maybe_players.append(player)
        elif player.availability is None:
            awaiting_players.append(player)
        else:
            unavailable_players.append(player)

    # Sort each list: in-team first, then alphabetically
    def in_team_sort_key(p):
        return (0 if p.is_selected else 1, p.name.lower())

    available_players.sort(key=in_team_sort_key)
    maybe_players.sort(key=in_team_sort_key)
    awaiting_players.sort(key=in_team_sort_key)
    unavailable_players.sort(key=in_team_sort_key)

    if request.method == 'POST':
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected')
        current_accordion = request.POST.get(
            'current_accordion', 'availablePlayers')

        if action == 'set_available':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': 'yes'}
                )
                match_player.availability = 'yes'
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) set to Available.')
            return redirect(
                f"{reverse('bulk_availability', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'set_maybe':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': 'maybe'}
                )
                match_player.availability = 'maybe'
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) set to Maybe.')
            return redirect(
                f"{reverse('bulk_availability', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'set_unavailable':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': 'no'}
                )
                match_player.availability = 'no'
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) set to Unavailable.')
            return redirect(
                f"{reverse('bulk_availability', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'add_to_team':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': None}
                )
                match_player.selected = True
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) added to team.')
            return redirect(
                f"{reverse('bulk_availability', args=[match_pk])}"
                f"?open={current_accordion}")

        elif action == 'remove_from_team':
            for player_id in selected_ids:
                match_player, created = MatchPlayer.objects.get_or_create(
                    match=current_match,
                    player_id=player_id,
                    defaults={'availability': None}
                )
                match_player.selected = False
                match_player.save()
            messages.success(
                request, f'{len(selected_ids)} player(s) removed from team.')
            return redirect(
                f"{reverse('bulk_availability', args=[match_pk])}"
                f"?open={current_accordion}")

    # Get which accordion to open from URL param
    open_accordion = request.GET.get('open', 'availablePlayers')

    # Count how many in each category are already in team
    in_team_count = len([p for p in available_players if p.is_selected])
    selectable_count = len(available_players) - in_team_count
    maybe_in_team = len([p for p in maybe_players if p.is_selected])
    awaiting_in_team = len([p for p in awaiting_players if p.is_selected])
    unavailable_in_team = len(
        [p for p in unavailable_players if p.is_selected])

    # Calculate selectable counts (not in team)
    maybe_selectable = len(maybe_players) - maybe_in_team
    awaiting_selectable = len(awaiting_players) - awaiting_in_team
    unavailable_selectable = len(unavailable_players) - unavailable_in_team

    return render(request, 'clubs/bulk_availability.html', {
        'match': current_match,
        'available_players': available_players,
        'maybe_players': maybe_players,
        'awaiting_players': awaiting_players,
        'unavailable_players': unavailable_players,
        'selected_count': selected_count,
        'selectable_count': selectable_count,
        'in_team_count': in_team_count,
        'maybe_in_team': maybe_in_team,
        'awaiting_in_team': awaiting_in_team,
        'unavailable_in_team': unavailable_in_team,
        'maybe_selectable': maybe_selectable,
        'awaiting_selectable': awaiting_selectable,
        'unavailable_selectable': unavailable_selectable,
        'open_accordion': open_accordion,
    })


@login_required
def match_list(request):
    """List all matches for user's club"""
    from django.db.models import Case, When, Value, IntegerField

    player = Player.objects.filter(user=request.user).first()
    if not player:
        return redirect('home')

    matches = Match.objects.filter(club=player.club).annotate(
        status_order=Case(
            When(status='scheduled', then=Value(0)),
            When(status='completed', then=Value(1)),
            When(status='cancelled', then=Value(2)),
            output_field=IntegerField(),
        )
    ).order_by('status_order', 'date')

    # Get current user's availability and selection status for each match
    for current_match in matches:
        mp = MatchPlayer.objects.filter(
            match=current_match, player=player).first()
        current_match.my_availability = mp.availability if mp else None
        current_match.is_selected = mp.selected if mp else False
        current_match.selected_count = current_match.match_players.filter(
            selected=True).count()
        current_match.available_count = current_match.match_players.filter(
            availability='yes', selected=False).count()
        current_match.maybe_count = current_match.match_players.filter(
            availability='maybe', selected=False).count()

    is_admin_or_captain = player.club.is_admin_or_captain(request.user)
    return render(request, 'clubs/match_list.html', {
        'matches': matches,
        'club': player.club,
        'is_admin_or_captain': is_admin_or_captain,
    })


@login_required
def player_list(request):
    """List all players for user's club"""
    player = Player.objects.filter(user=request.user).first()
    if not player:
        return redirect('home')

    players = Player.objects.filter(club=player.club, is_active=True)
    is_admin_or_captain = player.club.is_admin_or_captain(request.user)
    return render(request, 'clubs/player_list.html', {
        'players': players,
        'club': player.club,
        'is_admin_or_captain': is_admin_or_captain,
    })


@login_required
def my_availability(request):
    """Player updates their own availability across all matches"""
    from django.db.models import Case, When, Value, IntegerField

    player = Player.objects.filter(user=request.user).first()
    if not player:
        return redirect('home')

    matches = Match.objects.filter(club=player.club).annotate(
        status_order=Case(
            When(status='scheduled', then=Value(0)),
            When(status='completed', then=Value(1)),
            When(status='cancelled', then=Value(2)),
            output_field=IntegerField(),
        )
    ).order_by('status_order', 'date')

    # Get current availability and selected count for each match
    for current_match in matches:
        mp = MatchPlayer.objects.filter(
            match=current_match, player=player).first()
        current_match.my_availability = mp.availability if mp else None
        current_match.is_selected = mp.selected if mp else False
        current_match.selected_count = MatchPlayer.objects.filter(
            match=current_match, selected=True).count()

    if request.method == 'POST':
        match_ids = request.POST.getlist('matches')
        new_availability = request.POST.get('availability')
        team_action = request.POST.get('team_action')

        for match_id in match_ids:
            target_match = Match.objects.get(pk=match_id)
            mp, created = MatchPlayer.objects.get_or_create(
                match=target_match,
                player=player,
                defaults={'availability': 'maybe'}
            )

            if new_availability:
                mp.availability = new_availability
                mp.save()

            if team_action == 'add':
                mp.selected = True
                mp.save()
            elif team_action == 'remove':
                mp.selected = False
                mp.save()

        if new_availability:
            messages.success(request, 'Availability updated successfully.')
        elif team_action == 'add':
            messages.success(request, 'Added to team.')
        elif team_action == 'remove':
            messages.success(request, 'Removed from team.')

        return redirect('my_availability')

    is_admin_or_captain = player.club.is_admin_or_captain(request.user)

    return render(request, 'clubs/my_availability.html', {
        'matches': matches,
        'player': player,
        'is_admin_or_captain': is_admin_or_captain,
    })


@login_required
def player_availability(request, player_pk):
    """Admin/captain updates a player's availability across all matches"""
    from django.db.models import Case, When, Value, IntegerField

    player = get_object_or_404(Player, pk=player_pk)

    # Permission check
    if not player.club.is_admin_or_captain(request.user):
        raise PermissionDenied

    matches = Match.objects.filter(club=player.club).annotate(
        status_order=Case(
            When(status='scheduled', then=Value(0)),
            When(status='completed', then=Value(1)),
            When(status='cancelled', then=Value(2)),
            output_field=IntegerField(),
        )
    ).order_by('status_order', 'date')

    # Get current availability for each match
    for current_match in matches:
        mp = MatchPlayer.objects.filter(
            match=current_match, player=player).first()
        current_match.my_availability = mp.availability if mp else None
        current_match.is_selected = mp.selected if mp else False
        current_match.selected_count = MatchPlayer.objects.filter(
            match=current_match, selected=True).count()

    if request.method == 'POST':
        match_ids = request.POST.getlist('matches')
        new_availability = request.POST.get('availability')
        team_action = request.POST.get('team_action')

        for match_id in match_ids:
            target_match = Match.objects.get(pk=match_id)
            mp, created = MatchPlayer.objects.get_or_create(
                match=target_match,
                player=player,
                defaults={'availability': 'maybe'}
            )

            if new_availability:
                mp.availability = new_availability
                mp.save()

            if team_action == 'add':
                mp.selected = True
                mp.save()
            elif team_action == 'remove':
                mp.selected = False
                mp.save()

        if new_availability:
            messages.success(request, 'Availability updated successfully.')
        elif team_action == 'add':
            messages.success(request, 'Added to team.')
        elif team_action == 'remove':
            messages.success(request, 'Removed from team.')

        return redirect('player_availability', player_pk=player_pk)

    return render(request, 'clubs/my_availability.html', {
        'matches': matches,
        'player': player,
        'is_admin_view': True,
    })
