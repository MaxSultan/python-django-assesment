from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory

import movies
from movies.models import Movie, Rating


def MovieListView(request):
    msg = request.GET.get('msg')
    return render(request, "movie/home.html",
                  {"movies": Movie.objects.all(), "movie_num": Movie.objects.count(), "msg": msg})


def MovieDetailView(request, id):
    movie = Movie.objects.get(pk=id)
    redirect('home')
    msg = request.GET.get('msg')
    return render(request, "movie/detail.html", {"movie": movie, "msg": msg})


MovieForm = modelform_factory(Movie, exclude=['avg_rating'])


def MovieCreateView(request):
    err_msg = 'The creation has failed.'
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            data = form.save()
            return redirect(f"/movies/{data.id}")
    else:
        form = MovieForm()
    return render(request, "movie/new.html", {"form": form, "msg": err_msg})


def delete(request, id):
    movie = Movie.objects.get(id=id)
    err_msg = 'The deletion has failed'
    success_msg = 'The movie has been successfully deleted!'
    if movie.delete():
        return redirect(f"/movies?msg={success_msg}")
    return redirect(f"/movies?msg={err_msg}")


def MovieUpdateView(request, id):
    movie = Movie.objects.get(id=id)
    return render(request, 'movie/edit.html', {'movieData': movie})


def update(request, id):
    movie = Movie.objects.get(id=id)
    movie_form = MovieForm(request.POST or None, instance=movie)
    if movie_form.is_valid():
        movie_form.save()
        msg = 'The movie has been successfully updated!'
        return redirect(f'/movies/{id}?msg={msg}',)
    return render(request, 'movie/edit.html', {'movieData': movie, "err_msg": 'The update has failed'})


def ratings(request, id):
    movie = Movie.objects.get(id=id)
    all_ratings = Rating.objects.raw("SELECT * FROM movies_rating WHERE movie_id = %s", [id])
    return render(request, 'movie/ratings.html', {"ratings": all_ratings, "movie": movie})


RatingForm = modelform_factory(Rating, exclude=[])


def add_rating(request, id):
    movie = Movie.objects.get(id=id)
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            data = form.save()
            return redirect(f"/movies/{data.movie_id}/ratings")
    else:
        form = RatingForm()
    return render(request, "movie/add_rating.html", {"form": form, "movie": movie})


def sort_by_release_date(request):
    movies = Movie.objects.raw("SELECT * FROM movies_movie ORDER BY date DESC")
    return render(request, "movie/release_date.html", {"movies": movies})


def sort_by_rating(request):
    movies = Movie.objects.raw("SELECT * FROM movies_movie ORDER BY avg_rating DESC")
    return render(request, "movie/sort_by_rating.html", {"movies": movies})


def search(request):
    query = request.GET.get('search')
    search_items = Movie.objects.raw("SELECT * FROM movies_movie WHERE title = %s", [query])
    return render(request, "movie/search.html", {"search_items": search_items, "query": query})
