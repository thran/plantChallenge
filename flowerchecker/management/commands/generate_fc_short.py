import json
from optparse import make_option
from clint.textui import progress
from django.core.management import BaseCommand
from data.parser import parse_flower
from flowerchecker.models import Answer


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
        SURNESS = 90

        terms = [t["id"] for t in json.load(open("data/final/terms-short.json"))["terms"]]
        flashcards = []
        contexts = []

        answers = Answer.objects.filter(sureness__gte=SURNESS).select_related("request")\
                      .prefetch_related("request__images").order_by("-request")
        for answer in progress.bar(answers, every=max(1, answers.count() / 100)):
            if answer.request.images.all().count() == 0:
                continue
            term, _ = parse_flower(answer.answer)
            if term not in terms:
                continue

            images = []
            for image in answer.request.images.all():
                if image.type == "original" and image.accesshash is not None:
                    images.append(image.accesshash + "-" + str(image.imgorder))
            if len(images) == 0:
                continue

            gps = answer.request.gps.split(" ")

            flashcards.append({
                "id": str(answer.request_id),
                "term": term,
                "context": str(answer.request_id),
            })

            contexts.append({
                "id": str(answer.request_id),
                "name-en": "",
                "fullname": answer.answer,
                "content-en": json.dumps(images),
                "lat": float(gps[0]),
                "long": float(gps[1])
            })

        json.dump({"contexts": contexts, "flashcards": flashcards}, open("data/final/flashcards-short.json", "w"), indent=4)