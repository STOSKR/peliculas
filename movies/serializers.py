from rest_framework import serializers
from movies.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["imdbID", "Title", "Year", "Poster", "added_at"]
        read_only_fields = ["added_at"]


class FavoriteCreateSerializer(serializers.Serializer):
    imdbID = serializers.CharField(max_length=20)
    Title = serializers.CharField(max_length=255)
    Year = serializers.CharField(max_length=10, required=False, default="")
    Poster = serializers.URLField(required=False, default="")
