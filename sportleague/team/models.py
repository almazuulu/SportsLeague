from django.db import models
from django.db.models import Count, F, Value
import uuid


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

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
        for team in [self.team_1, self.team_2]:
            # Calculate points as shown previously
            wins_as_team_1 = Game.objects.filter(team_1=team, team_1_score__gt=F('team_2_score')).count()
            wins_as_team_2 = Game.objects.filter(team_2=team, team_2_score__gt=F('team_1_score')).count()
            draws_as_team_1 = Game.objects.filter(team_1=team, team_1_score=F('team_2_score')).count()
            draws_as_team_2 = Game.objects.filter(team_2=team, team_1_score=F('team_2_score')).count()
            total_points = (wins_as_team_1 + wins_as_team_2) * 3 + (draws_as_team_1 + draws_as_team_2)

            # Update the team's points
            team.points = total_points
            team.save()
            
    def __str__(self):
        return f"{self.team_1} {self.team_1_score} - {self.team_2_score} {self.team_2}"

