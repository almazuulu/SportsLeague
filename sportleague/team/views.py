from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
import csv
from .models import Game, Team
from .forms import UploadCSVForm
from io import TextIOWrapper



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
    
    

    
    
