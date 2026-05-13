from django.db import models
from .story import Story
from .haunting_type import HauntingType


class StoryHauntingType(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    haunting_type = models.ForeignKey(HauntingType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("story", "haunting_type")
