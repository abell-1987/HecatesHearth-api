from django.db import models


class State(models.Model):
    abbreviation = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.abbreviation
