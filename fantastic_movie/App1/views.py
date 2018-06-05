from __future__ import unicode_literals

import http.client
import json
import pdb
import time
import urllib.request

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from App1.forms import MovieForm, NewMovieForm, SearchMovieForm
from App1.models import Actor, Director, Genre, Movie

# ajax
from django.http import JsonResponse
from django.template.loader import render_to_string
from django import views

class Ajax(views.View):
    template_name = 'movies/index.html'
    def get(self, request):
        if request.is_ajax():
            query = request.GET.get('q')
            if query:
                context = {'movies': Movie.objects.filter(
                        Q(title__icontains=query) |
                        Q(director__name__icontains=query) |
                        Q(actors__name__icontains=query) |
                        Q(genres__name__icontains=query)
                        ).distinct()
                    }
            else:
                context = {'movies' : Movie.objects.all() }
			
        return render(request,self.template_name, {'movies': context})


# Create your views here.
def API(request):
    if not request.user.is_superuser:
        raise Http404

    conn = http.client.HTTPSConnection("api.themoviedb.org")
    API_KEY = "0b2c4ff39ce70fc79faf50910fc75d54"
    MOVIE_ID = ""
    PAGE = "1"

    # top rated movies
    conn.request("GET", "/3/movie/top_rated?api_key=" + API_KEY + "&language=en-US&page=" + PAGE)
    res = conn.getresponse()
    data = res.read()
    obj = data.decode("utf-8")
    jsonObjTop = json.loads(obj)
    for item in jsonObjTop['results']:
        MOVIE_ID = item['id']
        
        movie = Movie.objects.filter(title=item['title'])
        #print(len(movie))
        #print(isinstance(movie[0], Movie))
        if len(movie) == 0:
            # movie search 1. provjeriti da li postoji u bazi po IMENU
            conn.request("GET", "/3/movie/" + str(MOVIE_ID) + "?api_key=" + API_KEY + "&language=en-US")
            res = conn.getresponse()
            data = res.read()
            obj = data.decode("utf-8")
            jsonObj = json.loads(obj)

            movie = Movie(
                title= jsonObj['title'],
                overview = jsonObj['overview'],
                poster_path = jsonObj['poster_path'],
                release_date = jsonObj['release_date'],
                budget = jsonObj['budget'],
                revenue = jsonObj['revenue'],
                runtime = jsonObj['runtime'],
                vote_average = jsonObj['vote_average'],
                vote_count = jsonObj['vote_count'],     
            )

            movie.save()

            # genre search
            genres = jsonObj['genres']
            for item in genres:
                genre = Genre.objects.filter(name=item['name'])
                if not genre:
                    genre = Genre(
                        name = item['name']
                    )
                    genre.save()
                else:
                    genre = genre[0]
                
                movie.genres.add(genre)
            
            # sleep je potreban radi previse slanja upita prema apiu
            time.sleep(2) 
            # director and actor search
            conn.request("GET", "/3/movie/" + str(MOVIE_ID) + "/credits?api_key=" + API_KEY)
            res = conn.getresponse()
            data = res.read()
            obj = data.decode("utf-8")
            jsonObj = json.loads(obj)
            
            for i in range(0,3):
                actorId = jsonObj['cast'][i]['id']
                actor = Actor.objects.filter(id=actorId)
                if not actor:
                    time.sleep(1) 
                    conn.request("GET", "/3/person/"+ str(actorId) +"?api_key=" + API_KEY)
                    res = conn.getresponse()
                    data = res.read()
                    obj = data.decode("utf-8")
                    jsonObjActor = json.loads(obj)
                    actor = Actor(
                        name = jsonObjActor['name'],
                        birth_date = jsonObjActor['birthday'],
                        gender = jsonObjActor['gender'],
                        place_of_birth = jsonObjActor['place_of_birth'],
                        biography = jsonObjActor['biography'],
                        profile_path = jsonObjActor['profile_path']
                    ) 
                    actor.save()
                else:
                    actor = actor[0]
                movie.actors.add(actor)

            for item in jsonObj['crew']:
                if item['job'] == 'Director':
                    director = Director.objects.filter(name=item['name'])
                    if not director:
                        conn.request("GET", "/3/person/" + str(item['id']) +"?api_key=" + API_KEY)
                        res = conn.getresponse()
                        data = res.read()
                        obj = data.decode("utf-8")
                        jsonObj = json.loads(obj)
                        director = Director(
                            name = jsonObj['name'],
                            birth_date = jsonObj['birthday'],
                            gender = jsonObj['gender'],
                            place_of_birth = jsonObj['place_of_birth'],
                            biography = jsonObj['biography'],
                            profile_path = jsonObj['profile_path']
                        ) 
                        director.save()
                    else:
                        director = director[0]
                    
                    movie.director = director
                    break
            
            movie.save()

    return HttpResponse(obj, content_type="application/json")


def details(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {'movie': Movie.objects.filter(id=id)}
    return render(request, 'movies/details.html', context)

def index(request):
    query = request.GET.get('q')
    if query:
        context = {'movies': Movie.objects.filter(
                Q(title__icontains=query) |
                Q(director__name__icontains=query) |
                Q(actors__name__icontains=query) |
                Q(genres__name__icontains=query)
                ).distinct()
            }
    else:
        context = {'movies' : Movie.objects.all() }
    
    paginator = Paginator(context['movies'], 10) # Show 25 contacts per page
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    
    return render(request, 'movies/index.html', {'movies': movies})

def new(request):
    if not request.user.is_superuser:
        raise Http404
    if request.method == 'POST':
        form = NewMovieForm(request.POST)
        #pdb.set_trace()
        if form.is_valid():
            form.save()
            return redirect('movies')
    else:
        form = NewMovieForm()

    return render(request, 'movies/new.html', {'form': form})

def edit(request, id):
    if not request.user.is_superuser or not request.user.is_staff:
        raise Http404
    movie=get_object_or_404(Movie, pk = id)
    #form = MovieForm(instance=movie)
    form = MovieForm(data = request.POST or None, instance=movie)
    #form = MovieForm(request.POST)
    #form = MovieForm(request.POST, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('movies')

    return render(request, 'movies/edit.html', {'form': form})

def delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    movie = get_object_or_404(Movie, pk = id)
    # movie = Movie.objects.get(pk=id)
    # Movie.objects.all().delete() 
    movie.delete()
    return redirect('movies')
    
def search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    params = {}
    query = request.GET
    for item in query:
        if query[item] is not None and query[item] != '':
            if item == 'title':
                params[str(item)] = query[item]
            elif item == 'release_date_before':
                params[str(item) + '__lte'] = query[item]
            elif item == 'release_date_after':
                params[str(item) + '__gte'] = query[item]
            elif item == 'budget':
                params[str(item) + '__gte'] = query[item]
            elif item == 'revenue':
                params[str(item) + '__gte'] = query[item]
            elif item == 'runtime':
                params[str(item) + '__lte'] = query[item]
            elif item == 'vote_average_min':
                params['vote_average' + '__gte'] = query[item]
            elif item == 'vote_average_max':
                params['vote_average' + '__lte'] = query[item]
            elif item == 'director':
                params[str(item) + '__name'] = query[item]
            elif item == 'actors':
                params[str(item) + '__name'] = query[item]
            elif item == 'genres':
                params[str(item) + '__name'] = query[item]

    #pdb.set_trace()
    movies = Movie.objects.filter(**params)

    if query and movies:
        context = {'movies': movies}
        return render(request, 'movies/index.html', context)
    else:
        context = {'movies' : Movie.objects.all() }
    
    return render(request, 'movies/search.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies')
    else:
        form = UserCreationForm()    
    return render(request, 'registration/registration.html', {'form': form})
