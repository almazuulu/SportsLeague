from django.contrib import admin
from .models import Team, Game

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        exclude=('id',)
        

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        exclude=('id',)

        
