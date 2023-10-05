from django.urls import path  
from . import views

urlpatterns = [
    path('', views.UploadCSVView.as_view(), name='home'),
    path('games/', views.GamesEditView.as_view(), name='games'),
]
