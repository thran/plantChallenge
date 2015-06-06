import json
from django.core.management import BaseCommand
from flowerchecker.models import Answer
from contest import models
from data.parser import parse_flower
from practice.models import ExtendedTerm


class Command(BaseCommand):

    def handle(self, *args, **options):
        for r in models.Request.objects.filter(answer__isnull=True):
            answer = Answer.objects.filter(request=r.original_id).first()
            if answer is None:
                continue
            parsed = parse_flower(answer.answer)
            r.answer = answer.answer
            term = ExtendedTerm.objects.filter(name=parsed[0]).first()
            if term:
                r.term = term
            else:
                self.stdout.write('Term not found for {}'.format(r.answer))
            r.save()
