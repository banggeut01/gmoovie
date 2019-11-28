from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/',views.detail,name='detail'),
    path('<int:movie_pk>/reviews/review_create/',views.review_create,name='review_create'),
    path('<int:movie_pk>/reviews/<int:review_pk>/delete/',views.delete,name='delete'),
    path('<int:movie_pk>/like/',views.like,name='like'),
    path('like_movies/', views.like_movies, name='like_movies'),
    path('<int:movie_pk>/wish/', views.wish, name='wish'),
    path('<int:account_pk>/wishs/', views.wishs, name='wishs'),
    path('search/', views.search, name='search'),
    path('top_movies/', views.top_movie, name='top_movie'),
    path('now_playing/', views.now_playing, name='now_playing'),
    path('up_coming/',views.up_coming, name='up_coming'),
    path('people_movies/<int:people_pk>/', views.people_movies, name='people_movies'),
    path('popular/', views.popular, name='popular'),
]