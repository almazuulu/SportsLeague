import csv
from io import TextIOWrapper
from typing import Any

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView

from .forms import CustomUserCreationForm, GameEditForm, GameForm, UploadCSVForm
from .models import Game, Team


class UploadCSVView(FormView):
    template_name = 'team/index.html'
    form_class = UploadCSVForm
    success_url = reverse_lazy('games')

    def form_valid(self, form):
        csv_file = TextIOWrapper(form.cleaned_data['csv_file'].file, encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            team_1_name, team_1_score, team_2_name, team_2_score = row
            team_1, _ = Team.objects.get_or_create(name=team_1_name)
            team_2, _ = Team.objects.get_or_create(name=team_2_name)

            Game.objects.create(
                team_1=team_1, team_1_score=team_1_score,
                team_2=team_2, team_2_score=team_2_score
            )
        messages.success(self.request, 'CSV File was successfully uploaded!')
        
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
        messages.success(self.request, 'Game details were successfully updated along with the Ranking!')
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
        if form.cleaned_data['team_1'] == 'new':
            team_1, _ = Team.objects.get_or_create(name=form.cleaned_data['team_1_new_name'])
        else:
            team_1 = Team.objects.get(pk=form.cleaned_data['team_1'])

        if form.cleaned_data['team_2'] == 'new':
            team_2, _ = Team.objects.get_or_create(name=form.cleaned_data['team_2_new_name'])
        else:
            team_2 = Team.objects.get(pk=form.cleaned_data['team_2'])

        self.object = form.save(commit=False)
        self.object.team_1 = team_1
        self.object.team_2 = team_2
        self.object.save()

        team_1.recalculate_points()
        team_2.recalculate_points()

        return super().form_valid(form)


class GameDeleteView(DeleteView):
    model = Game
    template_name = 'team/delete_game_confirm.html'
    success_url = reverse_lazy('games')

    def post(self, request, *args, **kwargs):
        game = self.get_object()
        team_1, team_2 = game.team_1, game.team_2

        response = super().post(request, *args, **kwargs)

        team_1.recalculate_points()
        team_2.recalculate_points()

        if not Game.objects.filter(team_1=team_1).exists() and not Game.objects.filter(team_2=team_1).exists():
            team_1.delete()

        if not Game.objects.filter(team_1=team_2).exists() and not Game.objects.filter(team_2=team_2).exists():
            team_2.delete()

        # Adding the success message
        messages.success(request, f"Game <strong>\"{team_1} {game.team_1_score} - {team_2} {game.team_2_score}\"</strong> has been removed. Rankings updated.")

        return response



class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! You can now login.')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for errors in form.errors.values():
            for error in errors:
                messages.error(self.request, error)
        return response
