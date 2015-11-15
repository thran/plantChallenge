from optparse import make_option
from django.core.management import BaseCommand
from proso_flashcards.models import Term, Context, Flashcard, Category
from proso_models.models import Item, Answer, Variable
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
        make_option(
            '--baditems',
            dest='baditems',
            action='store_true',
            default=False,
            help='clear all item which are not connected to any object'),
        make_option(
            '--badvariables',
            dest='badvariables',
            action='store_true',
            default=False,
            help='clear all variables which are not connected to environment info'),
    )

    def handle(self, *args, **options):
        if options["items"]:
            Item.objects.all().delete()
        if options["idterms"]:
            for t in Term.objects.all():
                if t.identifier.isnumeric():
                    t.delete()
        if options["baditems"]:
            models = [Answer, Flashcard, Context, Term, Category]
            ids = set(Item.objects.all().values_list("pk", flat=True))
            for model in models:
                ids -= set(model.objects.all().values_list("item_id", flat=True))
            print "deleting", len(ids), "items"
            Item.objects.filter(pk__in=ids).delete()
        if options["badvariables"]:
            print "deleting", Variable.objects.filter(info__isnull=True).count(), "varibles"
            Variable.objects.filter(info__isnull=True).delete()
