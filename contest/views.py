from datetime import datetime, timedelta
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Prefetch, Sum
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from contest.models import Request, Guess, REQUEST_LIFETIME
from practice.models import ExtendedTerm, get_answer_counts_in_sets

ANSWERS_TO_OPEN_CONTEST = 20


def allow_user_to_contest(user):
    if user.is_anonymous():
        return False
    if user.is_staff:
        return True
    return max([0] + get_answer_counts_in_sets(user).values()) >= ANSWERS_TO_OPEN_CONTEST


@user_passes_test(allow_user_to_contest)
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


@user_passes_test(allow_user_to_contest)
def get_data(request):
    requests_objs = Request.objects.filter(bad=False, created__gt=datetime.now()-timedelta(seconds=REQUEST_LIFETIME))\
        .select_related("term")\
        .prefetch_related(Prefetch("guesses", queryset=Guess.objects.select_related("term").filter(user=request.user)))\
        .order_by("-created")

    guesses = Guess.objects.filter(user=request.user).order_by("-timestamp").select_related("request", "term", "request__term")

    leaderboard = []
    for u in User.objects.all().annotate(Sum("guesses__points")).filter(guesses__points__sum__isnull=False).order_by("-guesses__points__sum"):
        leaderboard.append({
            "name": u"{} {}".format(u.first_name, u.last_name),
            "points": u.guesses__points__sum,
            "self": u == request.user,
        })

    return JsonResponse({
        "requests": map(lambda r: r.to_json(request.user), list(requests_objs)),
        "request_lifetime": REQUEST_LIFETIME,
        "guesses": map(lambda g: g.to_json(), list(guesses)),
        "leaderboard": leaderboard,
        "total_points": Guess.objects.filter(points__isnull=False, user=request.user).aggregate(Sum("points"))["points__sum"],
    })
