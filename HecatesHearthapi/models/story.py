from django.db import models
from django.contrib.auth.models import User
from .location import Location
from .haunting_type import HauntingType


class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="stories"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    haunting_types = models.ManyToManyField(
        HauntingType, through="StoryHauntingType", related_name="stories"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
