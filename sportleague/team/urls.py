from django.urls import path  
from . import views

urlpatterns = [
    path('', views.UploadCSVView.as_view(), name='home'),
    path('games/', views.GamesEditView.as_view(), name='games'),
    path('ranking/', views.TeamRatingListView.as_view(), name='ranking'),
    path('create_game', views.CreateGameView.as_view(), name='create_game'),
    path('delete_game/<uuid:pk>/', views.GameDeleteView.as_view(), name='delete_game'),
]


