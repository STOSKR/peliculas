from django.urls import path
from movies.views import (
    MovieSearchView,
    MovieDetailView,
    FavoriteListView,
    FavoriteDetailView,
)

urlpatterns = [
    path("search/", MovieSearchView.as_view(), name="movie-search"),
    path("favorites/", FavoriteListView.as_view(), name="favorites-list"),
    path(
        "favorites/<str:imdbID>/",
        FavoriteDetailView.as_view(),
        name="favorites-detail",
    ),
    path("<str:movie_id>/", MovieDetailView.as_view(), name="movie-detail"),
]
