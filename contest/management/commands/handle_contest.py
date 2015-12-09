import json
from datetime import timedelta, datetime

from django.core import management
from django.core.management import BaseCommand
from flowerchecker.models import Answer
from contest import models
from data.parser import parse_flower
from practice.models import ExtendedTerm


class Command(BaseCommand):

    def handle(self, *args, **options):
        management.call_command('check_answers')
        management.call_command('evaluate_guesses')
        management.call_command('fetch_requests')
