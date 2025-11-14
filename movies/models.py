from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imdbID = models.CharField(max_length=20, primary_key=True)
    Title = models.CharField(max_length=255)
    Year = models.CharField(max_length=10, blank=True, default="")
    Poster = models.URLField(blank=True, default="")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "imdbID")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username} - {self.Title}"
