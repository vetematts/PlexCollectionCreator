from tmdbv3api import TMDb, Search, Collection
from functools import lru_cache


class TMDbSearch:
    def __init__(self, api_key):
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key
        self.tmdb.language = "en"
        self.tmdb.debug = True
        self.search = Search()

    @lru_cache(maxsize=128)
    def search_movies(self, keyword, limit=10):
        try:
            results = self.search.movies(keyword)
        except Exception as e:
            print(f"Error searching TMDb: {e}")
            return []

        movie_titles = []

        count = 0
        for movie in results:
            if hasattr(movie, "title"):
                title = movie.title
                if hasattr(movie, "release_date") and movie.release_date:
                    title = f"{title} ({movie.release_date[:4]})"
                movie_titles.append(title)
                count += 1
            if count >= limit:
                break

        return movie_titles

    @lru_cache(maxsize=32)
    def get_movies_from_collection(self, collection_id):
        try:
            collection = Collection()
            result = collection.details(collection_id)
        except Exception as e:
            print(f"Error fetching collection {collection_id}: {e}")
            return []

        movies = []
        for movie in result.get("parts", []):
            title = movie.get("title")
            date = movie.get("release_date")
            if title:
                if date and len(date) >= 4:
                    movies.append(f"{title} ({date[:4]})")
                else:
                    movies.append(title)
        return movies
