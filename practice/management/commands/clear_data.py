from optparse import make_option
from django.core.management import BaseCommand
from proso_models.models import Item


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--clear',
            dest='clear',
            action='store_true',
            default=False,
            help='do it'),
    )

    def handle(self, *args, **options):
        if options["clear"]:
            Item.objects.all().delete()