import json
from django.core.management import BaseCommand
import re
from flowerchecker.models import Request
from practice.models import ExtendedContext, ExtendedTerm


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = json.load(open("data/final/flashcards.json"))
        ids = []
        for term in ExtendedTerm.objects.all():
            if re.match('\w+ [A-Z]', term.identifier) is not None:
                print term.identifier, term.flashcards.all().count()
                if term.flashcards.all().count() > 0:
                    for fc in term.flashcards.all():
                        ids.append(fc.identifier)
                else:
                    term.delete()

        new_data = {"contexts": [], "flashcards": []}
        for context in data["contexts"]:
            if context["id"] in ids:
                new_data["contexts"].append(context)
        for flashcard in data["flashcards"]:
            if flashcard["id"] in ids:
                new_data["flashcards"].append(flashcard)

        json.dump(new_data, open("data/final/flashcards-case-fix.json", 'w'), indent=4)

