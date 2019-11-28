from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ReviewForm
from .models import Movie, Review, People, State, Wish

def index(request):
    if request.user.is_authenticated:
        user = request.user
        movies = Movie.objects.all()
        top_rate = []
        nowplaying = []
        upcoming = []
        recommend = []
        populars = []
        like_movies = user.like_movies.all()
        for like in like_movies:
            person = like.cast.all()
            for per in person:
                rec_movies = per.known_for.all()
                for rec_movie in rec_movies:
                    if rec_movie not in like_movies and rec_movie not in recommend:
                        recommend.append(rec_movie)
                        break
        popular_idx = [19404, 330457, 13398, 475557, 484468, 466282, 420809, 290859, 238628, 423204, 453405, 527641]
        for popular in popular_idx:
            for movie in movies:
                if popular == int(movie.pk):
                    populars.append(movie)
                    break
        for i in range(12):
            top_rate.append(movies[i])
        for movie in movies:
            if int(movie.category) & 2: # 현재 상영중
                if len(nowplaying) < 12:
                    nowplaying.append(movie)
            if int(movie.category) & 1: # 개봉 예정
                if len(upcoming) < 12:
                    upcoming.append(movie)
        if not recommend:
            recommend = nowplaying
        context = {
            'recommends': recommend,
            'populars': populars,
            'movies' : top_rate,
            'nowplaying': nowplaying,
            'upcoming': upcoming
        }
        return render(request,'movies/index.html',context)
    else:
        return redirect('accounts:login')

@login_required        
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
    states = State.objects.all()
    context = {
        'movie': movie,
        'review_form': review_form,
        'is_up': is_up,
        'is_now': is_now,
        'peoples': peoples,
        'states': states,
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

@login_required
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

@login_required
def like_movies(request):
    movies = request.user.like_movies.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/like_movies.html', context)

@login_required
def wish(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        print(request.POST)
        wish = Wish()
        wish.user = request.user
        wish.movie = movie
        wish.state_id = request.POST.get('state')
        wish.is_male = request.user.is_male
        wish.save()
        return redirect('movies:detail', movie_pk)
    else: # get
        wish = Wish.objects.filter(user=request.user, movie=movie_pk)
        movie.wish_users.remove(request.user)
        return redirect('movies:detail', movie_pk)

@login_required
def wishs(request, account_pk):
    # wishs = request.user.wish_movies.all()
    # context = {
        # 'wishs': wishs,
    # }
    wishs = Wish.objects.filter(user_id=account_pk)
    context = {
        'wishs': wishs,
    }
    return render(request, 'movies/wish.html', context)

def search(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    peoples = People.objects.all()
    word = request.GET.get('search')
    if word.is_valid():
        result_genres = []
        result_movies = []
        result_peoples = []
        genre_movies = []
        for genre in genres:
            if word in genre.name:
                result_genres.append(genre)
        if result_genres:
            for genre in result_genres:
                genre_movies = genre.movie_ids.all()
        for movie in movies:
            if word in movie.title:
                result_movies.append(movie)
        for people in peoples:
            if word in people.name:
                result_peoples.append(people)
        context = {
            'genres': genre_movies,
            'movies': result_movies,
            'peoples': result_peoples
        }
        
    return render(request,'movies/search.html', context)
        
def top_movie(request):
    results = []
    movies = Movie.objects.all()
    for i in range(99, 0, -1):
        for movie in movies:
            if str(float(i)/10)[:3] == str(movie.vote_average)[:3]:
                results.append(movie)
        if len(results) > 20:
            break
    context = {
        'top_movies': results,
    }
    return render(request,'movies/search.html', context)

def now_playing(request):
    results = []
    movies = Movie.objects.all()
    for movie in movies:
        if int(movie.category) & 2:
            results.append(movie)
    context = {
        'now_playing': results,
    }
    return render(request,'movies/search.html', context)

def up_coming(request):
    results = []
    movies = Movie.objects.all()
    for movie in movies:
        if int(movie.category) & 1:
            results.append(movie)
    context = {
        'up_coming': results,
    }
    return render(request,'movies/search.html', context)

def popular(request):
    results = []
    popular_idx = [429617, 330457, 480042, 475557, 453075, 466272, 420818, 290859, 474350, 423204, 453405, 283995, 384018]
    movies = Movie.objects.all()
    for pop in popular_idx:
        for movie in movies:
            if int(movie.pk) == pop:
                results.append(movie)
                break
    context = {
        'popular': results,
    }
    return render(request,'movies/search.html', context)

def people_movies(request, people_pk):
    people = get_object_or_404(People, pk=people_pk)
    movies = people.known_for.all()
    if len(movies) > 20: 
        movies = movies[:20]
    context = {
        'movies': movies,
        'people': people,
    }
    return render(request, 'movies/people.html', context)