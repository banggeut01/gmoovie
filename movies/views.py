from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ReviewForm
from .models import Movie, Review, People
# Create your views here.
# def index(request):
#     if request.user.is_authenticated:
#         movies = Movie.objects.all()
#         context = {
#             'movies' : movies
#         }
#         return render(request,'movies/index.html',context)
#     else:
#         return redirect('accounts:login')
def index(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all()
        nowplaying = []
        upcoming = []
        for movie in movies:
            if int(movie.category) & 2: # 현재 상영중
                nowplaying.append(movie)
            if int(movie.category) & 1: # 개봉 예정
                upcoming.append(movie)
        context = {
            'movies' : movies,
            'nowplaying': nowplaying,
            'upcoming': upcoming
        }
        return render(request,'movies/index.html',context)
    else:
        return redirect('accounts:login')
        
def detail(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    review_form = ReviewForm()
    is_now, is_up = False, False # 현재 상영중, 개봉 예정
    if int(movie.category) & 1: is_up = True
    if int(movie.category) & 2: is_now = True
    peoples = []
    casts = movie.cast.all()
    for cast in casts:
        people = People.objects.filter(id=cast.id).first()
        if people:
            peoples.append(people)
    context = {
        'movie': movie,
        'review_form': review_form,
        'is_up': is_up,
        'is_now': is_now,
        'peoples': peoples
    }
    
    return render(request,'movies/detail.html',context)

@require_POST
def review_create(request,movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie,pk=movie_pk)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = request.user
            form.movie = movie
            form.save()
            return redirect('movies:detail',movie_pk)
    else:
        return redirect('accounts:login')

@require_POST
def delete(request,movie_pk,review_pk):
    review = get_object_or_404(Review,pk=review_pk)
    if review.user == request.user:
        review.delete()
    return redirect('movies:detail',movie_pk)

@require_POST
def like(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.user.is_authenticated:
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
            
        return redirect('movies:detail', movie_pk)
    else:
        return redirect('accounts:login')