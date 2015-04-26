from optparse import make_option
from django.core.management import BaseCommand
from proso_flashcards.models import Term, Context, Flashcard
from proso_models.models import Item
from practice.models import ExtendedContext


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--items',
            dest='items',
            action='store_true',
            default=False,
            help='clear all items'),
        make_option(
            '--idterms',
            dest='idterms',
            action='store_true',
            default=False,
            help='clear all terms with int id'),
    )

    def handle(self, *args, **options):
        if options["items"]:
            Item.objects.all().delete()
        if options["idterms"]:
            for t in Term.objects.all():
                if t.identifier.isnumeric():
                    t.delete()