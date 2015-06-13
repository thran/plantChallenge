import json
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from practice.models import ExtendedTerm

@cache_page(60 * 60 * 24 * 30)
def typehead(request, exclude_short=True, exclude_long=False, complex=False):
    LIMIT = 5
    MIN_LENGHT = 2
    search = request.GET.get("search", None)
    if search is None or len(search) < MIN_LENGHT:
        return HttpResponseBadRequest()

    if complex:
        q = Q()
        for s in search.split(" "):
            q &= Q(name__icontains=s)
    else:
        q = Q(name__istartswith=search)
    if exclude_short:
        q &= Q(name__contains=" ")
    if exclude_long:
        q &= ~Q(name__contains=" ")
    data = {
        "plants": map(lambda t: t.to_json(nested=True), ExtendedTerm.objects.filter(q).order_by("name")[:LIMIT]),
        "count": max(0, ExtendedTerm.objects.filter(q).order_by("name").count() - LIMIT),
    }
    return JsonResponse(data)

def home(request):
    if not hasattr(request.user, "userprofile"):
        user = ""
    else:
        user = json.dumps(request.user.userprofile.to_json())
    return render(request, "index.html", {"user": user})