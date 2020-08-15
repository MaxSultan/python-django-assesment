from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('<int:id>', views.MovieDetailView, name='detail'),
    path('new', views.MovieCreateView, name='new'),
    path('edit/<int:id>', views.MovieUpdateView, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('<int:id>/ratings', views.ratings, name='ratings'),
    path('<int:id>/ratings/add_rating', views.add_rating, name='add_rating'),
    path('', views.MovieListView, name='home'),
    path('release_date', views.sort_by_release_date, name='release_date'),
    path('sort_by_rating', views.sort_by_rating, name='sort_by_rating'),
    path('search', views.search, name='search')
]