from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)

class People(models.Model):
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=140)
    
class Movie(models.Model):
    title = models.CharField(max_length=30)
    vote_average = models.FloatField()
    release_date = models.DateField() # 빈 곳 처리 blank=True, null=True
    overview = models.TextField()
    poster_path = models.CharField(max_length=140)
    backdrop_path = models.CharField(max_length=140)
    runtime = models.IntegerField()
    tagline = models.TextField()
    category = models.CharField(max_length=3) 
    genre_ids = models.ManyToManyField( # Movie-Genre N:M
        Genre, 
        related_name='movie_ids',
        blank=True)
    like_users = models.ManyToManyField( # Movie-User N:M 좋아요
        settings.AUTH_USER_MODEL,
        related_name='like_movies',
        blank=True
    )
    wish_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Wish', # 중개 모델
        related_name='wish_movies',
        blank=True
    )
    cast = models.ManyToManyField(
        People,
        related_name='known_for',
        blank=True
    )

class State(models.Model): # 지역1 : "서울"
    state = models.CharField(max_length=30)

class Area(models.Model): # 지역2 : "강남"
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    area = models.CharField(max_length=30)

class Wish(models.Model): # Movie-User N:M 보고싶어요
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_male = models.BooleanField() # 남:True, 여:False User 정보에도!
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

class Review(models.Model):
    content = models.CharField(max_length=140)
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)