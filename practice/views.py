from django.http import JsonResponse
from practice.models import ExtendedTerm


def typehead(request):
    LIMIT = 5
    data = {"plants": map(lambda t: t.to_json(nested=True),
                          ExtendedTerm.objects.filter(name__contains=request.GET.get("input"))
                          .order_by("name")[:LIMIT])}
    return JsonResponse(data)