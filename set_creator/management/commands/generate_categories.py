from collections import defaultdict
import json
from django.core.management import BaseCommand
from set_creator.models import Set


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = json.load(open("data/final/terms-clean.json"))
        categories = []
        terms = data["terms"]
        relationships = defaultdict(lambda: [])

        for s in Set.objects.all():
            categories.append({
                "id": str(s.pk),
                "name-en": s.name,
                "not-in-model": not s.active,
                "type": "set" if s.active else "set-deactivated",
            })
            for t in s.terms.all():
                relationships[t.identifier].append(str(s.pk))

        for term in terms:
            term["categories"] = relationships[term["id"]]

        json.dump({"terms": terms}, open("data/final/terms.json", "w"), indent=4)
        json.dump({"categories": categories}, open("data/final/categories.json", "w"), indent=4)