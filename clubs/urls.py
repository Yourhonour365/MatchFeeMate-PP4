from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Club CRUD routes
    path('club/new/', views.club_create, name='club_create'),
    path('club/<int:pk>/', views.club_detail, name='club_detail'),  # pk = primary key (club id)
    path('club/<int:pk>/edit/', views.club_update, name='club_update'),
    path('club/<int:pk>/delete/', views.club_delete, name='club_delete'),
    # Player CRUD routes
    path('club/<int:club_pk>/player/new/', views.player_create, name='player_create'),
    path('player/<int:pk>/edit/', views.player_update, name='player_update'),
    path('player/<int:pk>/delete/', views.player_delete, name='player_delete'),
    # Opposition CRUD routes
    path('club/<int:club_pk>/opposition/new/', views.opposition_create, name='opposition_create'),
    path('opposition/<int:pk>/edit/', views.opposition_update, name='opposition_update'),
    path('opposition/<int:pk>/delete/', views.opposition_delete, name='opposition_delete'),
    # Match CRUD routes
    path('club/<int:club_pk>/match/new/', views.match_create, name='match_create'),
    path('match/<int:pk>/', views.match_detail, name='match_detail'),
    path('match/<int:pk>/edit/', views.match_update, name='match_update'),
    path('match/<int:pk>/delete/', views.match_delete, name='match_delete'),
]