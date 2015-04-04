from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from practice.models import ExtendedTerm


def typehead(request):
    LIMIT = 5
    MIN_LENGHT = 2
    search = request.GET.get("search", None)
    if search is None or len(search) < MIN_LENGHT:
        return HttpResponseBadRequest()

    q = Q()
    for s in search.split(" "):
        q &= Q(name__icontains=s)
    data = {"plants": map(lambda t: t.to_json(nested=True),
                          ExtendedTerm.objects.filter(q)
                          .order_by("name")[:LIMIT])}
    return JsonResponse(data)