import requests
from django.conf import settings


class OMDBRepository:
    def __init__(self):
        self.base_url = settings.OMDB_BASE_URL
        self.api_key = settings.OMDB_API_KEY

    def search_movies(self, query, page=1):
        params = {"s": query, "page": page, "apikey": self.api_key}
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_movie_detail(self, imdbID):
        params = {"i": imdbID, "apikey": self.api_key}
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
