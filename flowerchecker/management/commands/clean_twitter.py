from django.core.management import BaseCommand
from flowerchecker.models import Request
from practice.models import ExtendedContext


class Command(BaseCommand):

    def handle(self, *args, **options):
        pks = Request.objects.exclude(source="mobile").values_list("pk", flat=True)
        ExtendedContext.objects.filter(identifier__in=list(pks)).delete()

