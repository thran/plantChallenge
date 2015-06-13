from collections import defaultdict
import json
import os
from shutil import copyfile
from django.core.management import BaseCommand, CommandError
from plantchallenge.settings import MEDIA_ROOT
from set_creator.models import Set


class Command(BaseCommand):

    def handle(self, *args, **options):
        directory = os.path.join(MEDIA_ROOT, "areas")
        if not os.path.exists(directory):
            os.makedirs(directory)

        categories = []
        terms = json.load(open("data/final/terms-clean.json"))["terms"] + json.load(open("data/final/terms-short.json"))["terms"]
        relationships = defaultdict(lambda: [])

        for s in Set.objects.filter(for_daniel=False, active=True):
            self._is_short(s)
            set_name = "set"
            categories.append({
                "id": str(s.pk),
                "name-en": s.name,
                "not-in-model": not s.active,
                "type": set_name if s.active else set_name + "-deactivated",
            })
            for t in s.terms.all():
                relationships[t.identifier].append(str(s.pk))

            if s.image:
                copyfile(os.path.join(MEDIA_ROOT, str(s.image)), os.path.join(directory, "{}.jpg".format(str(s.pk))))

        new_terms = []
        for term in terms:
            if len(relationships[term["id"]]) == 0:
                continue
            term["categories"] = relationships[term["id"]]
            new_terms.append(term)

        json.dump({"terms": new_terms}, open("data/final/terms.json", "w"), indent=4)
        json.dump({"categories": categories}, open("data/final/categories.json", "w"), indent=4)

    def _is_short(self, s):
        long = None
        for term in s.terms.all():
            if long is None:
                long = " " in term.name
            elif long != (" " in term.name):
                raise CommandError("Set {} contains both short and long terms".format(s.name))
        return not long
