from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from proso_flashcards.models import Term, Context, Flashcard


class ExtendedTerm(Term):
    class Meta:
        verbose_name = "Plant"

    url = models.TextField()
    interesting = models.TextField(null=True, blank=True)
    example = models.ForeignKey(Flashcard, null=True, blank=True)

    def to_json(self, nested=False):
        json = Term.to_json(self, nested)
        json["external_url"] = self.url
        json["interesting"] = self.interesting
        if self.example and not nested:
            json["example"] = self.example.to_json(nested=False, categories=False)
        return json

    @staticmethod
    def load_data(data, term):
        if 'url' in data:
            term.url = data["url"]
        if 'interesting' in data:
            term.interesting = data["interesting"]


class ExtendedContext(Context):
    class Meta:
        verbose_name = "Request"

    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)

    def to_json(self, nested=False, with_content=True):
        json = Context.to_json(self, nested, with_content)
        if self.lat and self.long:
            json["lat"] = int(self.lat)
        json["long"] = int(self.long)
        return json

    @staticmethod
    def load_data(data, context):
        if 'lat' in data and 'long' in data:
            context.lat = data["lat"]
            context.long = data["long"]
        if 'fullname' in data:
            context.fullname = data["fullname"]


class Request(Flashcard):
    class Meta:
        proxy = True


settings.PROSO_FLASHCARDS["term_extension"] = ExtendedTerm
settings.PROSO_FLASHCARDS["context_extension"] = ExtendedContext


@receiver(pre_save, sender=ExtendedTerm)
@receiver(pre_save, sender=ExtendedContext)
def create_items(sender, instance, **kwargs):
    pre_save.send(sender=sender.__bases__[0], instance=instance)