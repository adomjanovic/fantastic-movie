from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=2,null=True)
    place_of_birth = models.CharField(max_length=100, null=True)
    biography = models.TextField(null=True)
    profile_path = models.TextField(null=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=2, null=True)
    place_of_birth = models.CharField(max_length=100, null=True)
    biography = models.TextField(null=True)
    profile_path = models.TextField(null=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.TextField()
    release_date = models.DateField()
    budget = models.IntegerField()
    revenue = models.IntegerField()
    runtime = models.IntegerField()
    vote_average = models.DecimalField(max_digits=4, decimal_places=2)
    vote_count = models.IntegerField()
    director = models.ForeignKey('Director', on_delete=models.CASCADE, null=True)
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)


   #Movie.objects.all().delete() za brisanje svih 