from django import forms
from .models import Movie
from .models import Director

class MovieForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ['title', 'overview', 'director', 'vote_average', 'release_date', 'runtime', 'actors', 'genres']

class NewMovieForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ['title', 'overview', 'poster_path', 'release_date', 'budget', 'revenue', 'runtime', 'vote_average', 'vote_count', 'director', 'actors', 'genres']

class SearchMovieForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ['title', 'runtime', 'vote_average', 'director', 'actors', 'genres']

