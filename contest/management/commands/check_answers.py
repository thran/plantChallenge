import json
from datetime import timedelta, datetime

from django.core.management import BaseCommand
from flowerchecker.models import Answer
from contest import models
from data.parser import parse_flower
from practice.models import ExtendedTerm


class Command(BaseCommand):

    def handle(self, *args, **options):
        for r in models.Request.objects.filter(closed=False):
            answer = Answer.objects.filter(request=r.original_id).first()
            if answer is None:
                if r.created.replace(tzinfo=None) + timedelta(seconds=models.WAIT_TIME_TO_ANSWER) < datetime.now():
                    r.closed = True
                    r.save()
                continue
            parsed = parse_flower(answer.answer)
            r.answer = answer.answer
            term = ExtendedTerm.objects.filter(name=parsed[0]).first()
            r.closed = True
            if term:
                r.term = term
            else:
                self.stdout.write(u'Term not found for {}'.format(r.answer))
            r.save()
