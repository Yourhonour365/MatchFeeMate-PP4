from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Club, Player
from .forms import ClubForm, PlayerForm


def home(request):
    """Display the homepage"""
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
    if request.method == 'POST':
        club.delete()
        return redirect('home')
    return render(request, 'clubs/club_confirm_delete.html', {'club': club})

@login_required
def player_create(request, club_pk):
    """Create a new player for a specific club"""
    club = get_object_or_404(Club, pk=club_pk)
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
    club_pk = player.club.pk
    if request.method == 'POST':
        player.delete()
        return redirect('club_detail', pk=club_pk)
    return render(request, 'clubs/player_confirm_delete.html', {'player': player})