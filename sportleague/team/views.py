import csv
from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView
from django.views.generic import TemplateView, ListView, CreateView
from io import TextIOWrapper

from .models import Game, Team
from .forms import UploadCSVForm, GameForm


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
    
    
class GamesEditView(ListView):
    model = Game
    template_name = 'team/games.html'
    context_object_name = 'games'
    

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
        # Getting or creating trams based from names or selected ID
        def get_or_create_team(choice_key, new_name_key):
            choice = form.cleaned_data[choice_key]
            if choice == 'new':
                name = form.cleaned_data[new_name_key]
                team, _ = Team.objects.get_or_create(name=name)
            else:
                team = Team.objects.get(pk=choice)
            return team

        team_1 = get_or_create_team('team_1', 'team_1_new_name')
        team_2 = get_or_create_team('team_2', 'team_2_new_name')

        self.object = form.save(commit=False)
        self.object.team_1 = team_1
        self.object.team_2 = team_2
        self.object.save()

        return super().form_valid(form)
    
    
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

    