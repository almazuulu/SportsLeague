import csv
from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic import TemplateView, ListView, CreateView
from io import TextIOWrapper

from .models import Game, Team
from .forms import UploadCSVForm, GameForm, GameEditForm


class UploadCSVView(FormView):
    template_name = 'team/index.html'
    form_class = UploadCSVForm
    success_url = reverse_lazy('games')  # Ссылка на страницу после успешной загрузки CSV

    def form_valid(self, form):
        csv_file = TextIOWrapper(form.cleaned_data['csv_file'].file, encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            team_1_name, team_1_score, team_2_name, team_2_score = row
            team_1, created = Team.objects.get_or_create(name=team_1_name)
            team_2, created = Team.objects.get_or_create(name=team_2_name)

            game = Game(team_1=team_1, team_1_score=team_1_score, team_2=team_2, team_2_score=team_2_score)
            game.save()

        return super().form_valid(form)
    
class GamesListView(ListView):
    model = Game
    template_name = 'team/games.html'
    context_object_name = 'games'
    
    
class GameEditView(UpdateView):
    model = Game
    form_class = GameEditForm
    template_name = 'team/update_game.html'
    success_url = reverse_lazy('games')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Game'
        return context
    

class TeamRatingListView(ListView):
    model = Team
    template_name = 'team/ranking_list.html'
    context_object_name = 'teams'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Team.objects.all().order_by('-points', 'name')
    
    
class CreateGameView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'team/game_form.html'
    success_url = reverse_lazy('games')
    
    def form_valid(self, form):
        # Saving the changes
        response = super().form_valid(form)
        
        # Getting the old values before the update
        old_team_1 = self.object.team_1
        old_team_2 = self.object.team_2

        # Updating the game with new values from the form
        game = form.save()
        
        # Recalculating ranking for the old teams and new teams
        old_team_1.recalculate_points()
        old_team_2.recalculate_points()
        game.team_1.recalculate_points()
        game.team_2.recalculate_points()

        # Check and remove teams not involved in any games
        for team in [old_team_1, old_team_2, game.team_1, game.team_2]:
            if not Game.objects.filter(team_1=team).exists() and not Game.objects.filter(team_2=team).exists():
                team.delete()

        return response
    
    
class GameDeleteView(DeleteView):
    model = Game
    template_name = 'team/delete_game_confirm.html' # Template of confirmation
    success_url = reverse_lazy('games') 
    
    def post(self, request, *args, **kwargs):
        game = self.get_object()
        team_1 = game.team_1
        team_2 = game.team_2

        # Deleting the game
        response = super().post(request, *args, **kwargs)  

        # Recalculating ranking for both teams after deleting the game
        team_1.recalculate_points()
        team_2.recalculate_points()
        
        # Checking the other games of teams, if there are no more games in one of the team then we deleting from ranking
        if not Game.objects.filter(team_1=team_1).exists() and not Game.objects.filter(team_2=team_1).exists():
            team_1.delete()

        if not Game.objects.filter(team_1=team_2).exists() and not Game.objects.filter(team_2=team_2).exists():
            team_2.delete()

        return response

    