from django.test import TestCase
from django.urls import reverse
from .models import Team, Game
from django.core.files.uploadedfile import SimpleUploadedFile


# Unit tests for Models
class TeamModelTest(TestCase):

    def setUp(self):
        self.team1 = Team.objects.create(name="Team A", points=0)
        self.team2 = Team.objects.create(name="Team B", points=0)

    def test_team_creation(self):
        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(self.team1.points, 0)
        self.assertEqual(self.team2.points, 0)

    def test_recalculate_points(self):
        Game.objects.create(team_1=self.team1, team_2=self.team2, team_1_score=2, team_2_score=1)
        
        # Refresh the team data from the database to get updated points
        self.team1.refresh_from_db()
        self.team2.refresh_from_db()
        
        self.assertEqual(self.team1.points, 3)  # Team A won
        self.assertEqual(self.team2.points, 0)  # Team B lost

        Game.objects.create(team_1=self.team1, team_2=self.team2, team_1_score=1, team_2_score=1)
        
        # Refresh the team data again from the database to get updated points
        self.team1.refresh_from_db()
        self.team2.refresh_from_db()
        
        self.assertEqual(self.team1.points, 4)  # 1 point for draw
        self.assertEqual(self.team2.points, 1)  # 1 point for draw


class GameModelTest(TestCase):

    def setUp(self):
        self.team1 = Team.objects.create(name="Team A", points=0)
        self.team2 = Team.objects.create(name="Team B", points=0)

    def test_game_creation(self):
        game = Game.objects.create(team_1=self.team1, team_2=self.team2, team_1_score=2, team_2_score=1)
        
        # Checking if the game was created correctly
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(game.team_1, self.team1)
        self.assertEqual(game.team_2, self.team2)
        self.assertEqual(game.team_1_score, 2)
        self.assertEqual(game.team_2_score, 1)
        
        # Check if the points were recalculated correctly
        self.team1.refresh_from_db()
        self.team2.refresh_from_db()
        self.assertEqual(self.team1.points, 3)  # Team A won
        self.assertEqual(self.team2.points, 0)  # Team B lost


# Unit tests for Views
class TeamViewsTest(TestCase):

    def setUp(self):
        self.team1 = Team.objects.create(name="Team A", points=10)
        self.team2 = Team.objects.create(name="Team B", points=5)
        self.game = Game.objects.create(
            team_1=self.team1, team_2=self.team2, team_1_score=1, team_2_score=2
        )

    def test_upload_csv_view(self):
        self.assertEqual(Game.objects.count(), 1)

        data = 'Team A,1,Team B,2\nTeam B,3,Team A,4'
        csv_file = SimpleUploadedFile("file.csv", data.encode('utf-8'), content_type="text/csv")
        
        url = reverse('home')  
        response = self.client.post(url, {'csv_file': csv_file})
        
        self.assertEqual(response.status_code, 302)  
        
        # Check if two games were added from the CSV (total games in DB should be 3, including the initial one)
        self.assertEqual(Game.objects.count(), 3)


    def test_game_edit_view(self):
        url = reverse('edit_game', kwargs={'pk': self.game.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        updated_data = {
            'team_1': self.team2.id,
            'team_2': self.team1.id,
            'team_1_score': 4,
            'team_2_score': 5,
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)

        self.game.refresh_from_db()
        self.assertEqual(self.game.team_1, self.team2)
        self.assertEqual(self.game.team_2, self.team1)
        self.assertEqual(self.game.team_1_score, 4)
        self.assertEqual(self.game.team_2_score, 5)


    def test_team_rating_list_view(self):
        url = reverse('ranking')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        teams = list(response.context['teams'])
        self.assertEqual(teams, [self.team2, self.team1]) 


    def test_games_list_view(self):
        url = reverse('games')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.game, response.context['games'])
        
    
    def test_game_delete_view(self):
        url = reverse('delete_game', kwargs={'pk': self.game.id})

        response = self.client.post(url)
        
        # Check if the redirect is successful
        self.assertEqual(response.status_code, 302)

        # Check if the game was deleted
        self.assertFalse(Game.objects.filter(pk=self.game.id).exists())
        
        
    def test_game_create_view(self):
        url = reverse('create_game')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        game_data = {
            'team_1': self.team1.id,
            'team_2': self.team2.id,
            'team_1_score': 2,
            'team_2_score': 1,
        }
        response = self.client.post(url, game_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Game.objects.filter(team_1=self.team1, team_2=self.team2).exists())
        
