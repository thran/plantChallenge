from datetime import datetime, timedelta
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from lazysignup.decorators import allow_lazy_user
from contest.models import Request, Guess, REQUEST_LIFETIME
from practice.models import ExtendedTerm


@staff_member_required
def make_guess(request):
    if not request.method == "POST":
        return HttpResponseBadRequest("method must be POST")
    data = json.loads(str(request.body.decode('utf-8')))
    request_obj = get_object_or_404(Request, pk=data["request"])
    term = get_object_or_404(ExtendedTerm, pk=data["term"]["id"])
    guess, created = Guess.objects.get_or_create(
        user=request.user,
        request=request_obj,
        defaults={"term": term}
    )
    if not created:
        guess.timestamp = datetime.now()
        guess.term = term
        guess.save()

    return HttpResponse("OK")


@staff_member_required
def requests(request):
    requests_objs = Request.objects.filter(bad=False, created__gt=datetime.now()-timedelta(seconds=REQUEST_LIFETIME))\
        .select_related("term")\
        .prefetch_related(Prefetch("guesses", queryset=Guess.objects.select_related("term").filter(user=request.user)))\
        .order_by("-created")

    return JsonResponse({"requests": map(lambda r: r.to_json(request.user), list(requests_objs)), "request_lifetime": REQUEST_LIFETIME})


@staff_member_required
def guesses(request):
    guesses = Guess.objects.filter(user=request.user)

    return JsonResponse({"requests": map(lambda g: g.to_json(), list(guesses))})