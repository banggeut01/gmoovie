from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/',views.detail,name='detail'),
    path('<int:movie_pk>/reviews/new/',views.new,name='new'),
    path('<int:movie_pk>/reviews/<int:review_pk>/delete/',views.delete,name='delete'),
    path('<int:movie_pk>/like/',views.like,name='like'),
]