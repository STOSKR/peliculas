from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from movies.services.movie_service import MovieService


class MovieSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        page = request.query_params.get('page', 1)

        if not query:
            return Response(
                {'error': 'Query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        movie_service = MovieService()
        data = movie_service.search_movies(query, page)
        return Response(data, status=status.HTTP_200_OK)


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie_service = MovieService()
        data = movie_service.get_movie_detail(movie_id)
        return Response(data, status=status.HTTP_200_OK)
