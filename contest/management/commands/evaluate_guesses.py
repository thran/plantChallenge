from optparse import make_option
from datetime import datetime, timedelta
from django.core.management import BaseCommand
from contest.models import Guess, REQUEST_LIFETIME


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
        guesses = Guess.objects.filter(request__answer__isnull=False,
                                       request__created__lte=datetime.now()-timedelta(seconds=REQUEST_LIFETIME))
        if not options["all"]:
            guesses = guesses.filter(correct__isnull=True)
        for guess in guesses:
            guess.evaluate()
