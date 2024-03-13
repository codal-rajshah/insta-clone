from django.db import models


class TimeStampedModel(models.Model):
    """
    Pre-populated model with created and updated date
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
