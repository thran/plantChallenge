from optparse import make_option
from django.core.management import BaseCommand
from contest.models import Guess


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--all',
            dest='all',
            action='store_true',
            default=False,
            help='reevaluate all guesses'),
    )

    def handle(self, *args, **options):
        guesses = Guess.objects.filter(request__answer__isnull=False)
        if not options["all"]:
            guesses = guesses.filter(correct__isnull=True)
        for guess in guesses:
            guess.evaluate()
