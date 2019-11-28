from django.contrib import admin
from .models import Movie, Genre, Review, State, Wish
# Register your models here.

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(State)
admin.site.register(Wish)