from movies.repositories.omdb_repository import OMDBRepository


class MovieService:
    def __init__(self):
        self.omdb_repository = OMDBRepository()

    def search_movies(self, query, page=1):
        data = self.omdb_repository.search_movies(query, page)

        if data.get("Response") == "False":
            return {"Search": [], "totalResults": "0", "Response": "True"}

        return data

    def get_movie_detail(self, imdb_id):
        data = self.omdb_repository.get_movie_detail(imdb_id)

        if data.get("Response") == "False":
            return {"Error": data.get("Error", "Movie not found")}

        return data
