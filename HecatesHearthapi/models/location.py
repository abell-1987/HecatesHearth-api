from django.db import models
from django.contrib.auth.models import User
from .state import State


class Location(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name="locations")
    description = models.TextField()
    history = models.TextField(null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)
    is_famous = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state.abbreviation}"
