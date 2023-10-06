from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game, Team

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label="Select a CSV file")


class GameForm(forms.ModelForm):
    team_1 = forms.ChoiceField(
        choices=[], 
        label="Team 1",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    team_2 = forms.ChoiceField(
        choices=[], 
        label="Team 2",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    team_1_new_name = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'style': 'display: none;', 'class': 'form-control'})
    )
    team_2_new_name = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'style': 'display: none;', 'class': 'form-control'})
    )

    class Meta:
        model = Game
        fields = ['team_1_score', 'team_2_score']
        widgets = {
            'team_1_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'team_2_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        TEAM_CHOICES = [
            ('', '--Select--'),
            ('new', '-- Create New Team --'),
        ] + [(team.pk, team.name) for team in Team.objects.all()]

        self.fields['team_1'].choices = TEAM_CHOICES
        self.fields['team_2'].choices = TEAM_CHOICES

    def clean(self):
        cleaned_data = super().clean()

        team_1_choice = cleaned_data.get('team_1')
        team_2_choice = cleaned_data.get('team_2')
        team_1_new_name = cleaned_data.get('team_1_new_name')
        team_2_new_name = cleaned_data.get('team_2_new_name')

        if team_1_choice == 'new' and not team_1_new_name:
            self.add_error('team_1_new_name', 'Team 1 name is required if creating a new team.')

        if team_2_choice == 'new' and not team_2_new_name:
            self.add_error('team_2_new_name', 'Team 2 name is required if creating a new team.')

        return cleaned_data
    

class GameEditForm(forms.ModelForm):
    team_1 = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    team_2 = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    team_1_score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    team_2_score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Game
        fields = ['team_1', 'team_1_score', 'team_2', 'team_2_score']
        
        
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})