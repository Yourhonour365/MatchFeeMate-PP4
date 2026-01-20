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
]