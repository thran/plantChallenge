from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from proso_flashcards.models import Term, Context


class ExtendedTerm(Term):
    url = models.TextField()
    interesting = models.TextField(null=True, blank=True)

    def to_json(self, nested=False):
        json = Term.to_json(self, nested)
        json["url"] = self.url
        json["interesting"] = self.interesting
        return json

    @staticmethod
    def load_data(data, term):
        if 'url' in data:
            term.url = data["url"]
        if 'interesting' in data:
            term.interesting = data["interesting"]


class ExtendedContext(Context):
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def to_json(self, nested=False):
        json = Context.to_json(self, nested)
        return json

    @staticmethod
    def load_data(data, context):
        pass
        if 'lat' in data and 'long' in data:
            context.lat = data["lat"]
            context.long = data["long"]


settings.PROSO_FLASHCARDS["term_extension"] = ExtendedTerm
settings.PROSO_FLASHCARDS["context_extension"] = ExtendedContext


@receiver(pre_save, sender=ExtendedTerm)
@receiver(pre_save, sender=ExtendedContext)
def create_items(sender, instance, **kwargs):
    pre_save.send(sender=sender.__bases__[0], instance=instance)