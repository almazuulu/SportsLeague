from django.db import models
from django.db.models import Count, F, Value
import uuid


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def recalculate_points(self):
        # Calculating the wins and Draws
        wins_as_team_1 = Game.objects.filter(team_1=self, team_1_score__gt=F('team_2_score')).count()
        wins_as_team_2 = Game.objects.filter(team_2=self, team_2_score__gt=F('team_1_score')).count()
        draws_as_team_1 = Game.objects.filter(team_1=self, team_1_score=F('team_2_score')).count()
        draws_as_team_2 = Game.objects.filter(team_2=self, team_2_score=F('team_1_score')).count()
        
        # Total points calculating
        total_points = (wins_as_team_1 + wins_as_team_2) * 3 + (draws_as_team_1 + draws_as_team_2)

        # Updating the points
        self.points = total_points
        self.save()

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_1 = models.ForeignKey(Team, related_name="home_games", on_delete=models.CASCADE)
    team_1_score = models.PositiveIntegerField()
    team_2 = models.ForeignKey(Team, related_name="away_games", on_delete=models.CASCADE)
    team_2_score = models.PositiveIntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the game first

        # Recalculate points for the involved teams
        self.team_1.recalculate_points()
        self.team_2.recalculate_points()
        
    def __str__(self):
        return f"{self.team_1} {self.team_1_score} - {self.team_2_score} {self.team_2}"

