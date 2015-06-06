import json
from django.core.management import BaseCommand
from flowerchecker.models import Request, Imagefile
from contest import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            last_id = models.Request.objects.values("original_id").order_by("-original_id")[0]['original_id']
        except IndexError:
            last_id = 0

        for r in Request.objects.filter(id__gt=last_id).order_by("-created")[:100]:
            gps = map(float, r.gps.split())
            images = Imagefile.objects.filter(accesshash=r.access_hash, type="original").values_list("imgorder", flat=True)
            request = models.Request(
                original_id=r.id,
                lat=gps[0],
                long=gps[1],
                images=json.dumps(map(lambda i: '{}-{}'.format(r.access_hash, i), images))
            )
            request.save()
            self.stdout.write('{} fetch'.format(request))
