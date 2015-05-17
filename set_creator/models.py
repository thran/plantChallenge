from django.db import models
from practice.models import ExtendedTerm


class Set(models.Model):
    name = models.CharField(max_length=255)
    terms = models.ManyToManyField(ExtendedTerm)
    active = models.BooleanField(default=True)
    for_daniel = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
