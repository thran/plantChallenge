from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from lazysignup.decorators import allow_lazy_user
from contest.models import Request, Guess, REQUEST_LIFETIME
from practice.models import ExtendedTerm


@allow_lazy_user
def make_guess(request):
    if not request.method == "GET":
        return HttpResponseBadRequest("method must be GET")
    request = get_object_or_404(Request, pk=request.GET.get("request", 0))
    if Guess.objects.filter(request=request, user=request.user).first():
        return HttpResponseBadRequest("guess already made")
    term = get_object_or_404(ExtendedTerm, pk=request.GET.get("term", 0))
    Guess.objects.create(
        user=request.user,
        term=term,
        request=request,
    )

    return HttpResponse("OK")


def requests(request):
    requests = Request.objects.filter(bad=False,
                                  created__gt=datetime.now()-timedelta(seconds=REQUEST_LIFETIME)).order_by("-created")

    return JsonResponse({"requests": map(lambda r: r.to_json(), list(requests)), "request_lifetime": REQUEST_LIFETIME})


def guesses(request):
    guesses = Guess.objects.filter(user=request.user)

    return JsonResponse({"requests": map(lambda g: g.to_json(), list(guesses))})