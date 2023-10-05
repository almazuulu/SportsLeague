from django.db import models
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

    # def save(self, *args, **kwargs):
    #     # Можно добавить логику пересчета очков прямо здесь, 
    #     # когда игра добавляется или обновляется.
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_1} {self.team_1_score} - {self.team_2_score} {self.team_2}"

