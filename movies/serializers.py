from rest_framework import serializers
from movies.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["imdb_id", "title", "year", "poster", "added_at"]
        read_only_fields = ["added_at"]


class FavoriteCreateSerializer(serializers.Serializer):
    imdb_id = serializers.CharField(max_length=20)
    title = serializers.CharField(max_length=255)
    year = serializers.CharField(max_length=10, required=False, default="")
    poster = serializers.URLField(required=False, default="")
