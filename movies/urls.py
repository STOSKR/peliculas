from django.urls import path
from movies.views import MovieSearchView, MovieDetailView

urlpatterns = [
    path("search/", MovieSearchView.as_view(), name="movie-search"),
    path("<str:movie_id>/", MovieDetailView.as_view(), name="movie-detail"),
]
