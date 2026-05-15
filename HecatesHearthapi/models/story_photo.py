from django.db import models
from django.contrib.auth.models import User
from .story import Story
from .location import Location


class StoryPhoto(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="photos")
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="story_photos"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="story_photos"
    )
    image = models.FileField(upload_to="story_photos")
    uploaded_at = models.DateTimeField(auto_now_add=True)
