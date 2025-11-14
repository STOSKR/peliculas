from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from movies.services.movie_service import MovieService
from movies.models import Favorite
from movies.serializers import FavoriteSerializer, FavoriteCreateSerializer
from django.db import IntegrityError


class MovieSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("query")
        page = request.query_params.get("page", 1)

        if not query:
            return Response(
                {"error": "Query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movie_service = MovieService()
        data = movie_service.search_movies(query, page)
        return Response(data, status=status.HTTP_200_OK)


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie_service = MovieService()
        data = movie_service.get_movie_detail(movie_id)
        return Response(data, status=status.HTTP_200_OK)


class FavoriteListView(APIView):
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite = Favorite.objects.create(
                user=request.user, **serializer.validated_data
            )
            return Response(
                FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {"error": "Esta película ya está en favoritos"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FavoriteDetailView(APIView):
    def delete(self, request, imdb_id):
        try:
            favorite = Favorite.objects.get(user=request.user, imdb_id=imdb_id)
            favorite.delete()
            return Response({"message": "Película eliminada de favoritos"})
        except Favorite.DoesNotExist:
            return Response(
                {"error": "Película no encontrada en favoritos"},
                status=status.HTTP_404_NOT_FOUND,
            )
