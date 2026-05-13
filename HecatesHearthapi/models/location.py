from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    description = models.TextField()
    history = models.TextField(null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "city", "state")

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"
