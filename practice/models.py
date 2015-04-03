from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from proso_flashcards.models import Term, Context


class ExtendedTerm(Term):
    url = models.TextField()

    def to_json(self, nested=False):
        json = Term.to_json(self, nested)
        json["url"] = self.url
        return json

    @staticmethod
    def load_data(data, term):
        if 'url' in data:
            term.url = data["url"]


class ExtendedContext(Context):

    def to_json(self, nested=False):
        json = Context.to_json(self, nested)
        return json

    @staticmethod
    def load_data(data, context):
        pass
        # if 'extra-info' in data:
        #     context.extra_info = data["extra-info"]


settings.PROSO_FLASHCARDS["term_extension"] = ExtendedTerm
settings.PROSO_FLASHCARDS["context_extension"] = ExtendedContext


@receiver(pre_save, sender=ExtendedTerm)
@receiver(pre_save, sender=ExtendedContext)
def create_items(sender, instance, **kwargs):
    pre_save.send(sender=sender.__bases__[0], instance=instance)