import json
from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import models
from practice.models import ExtendedTerm

REQUEST_LIFETIME = 24 * 60 * 60
WAIT_TIME_TO_ANSWER = 3 * 24 * 60 * 60
MAX_POINTS = 100


class Request(models.Model):
    original_id = models.IntegerField(unique=True)
    images = models.TextField()
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    bad = models.BooleanField(default=False)

    term = models.ForeignKey(ExtendedTerm, null=True)
    answer = models.TextField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    def __unicode__(self):
        return "request {}".format(self.original_id)

    def to_json(self, nested=True, without_guess=False):
        data = {
            "id": self.pk,
            "images": json.loads(self.images),
            "lat": int(self.lat),
            "long": int(self.long),
            "created": self.created,
        }
        if self.term and nested and (self.created.replace(tzinfo=None) + timedelta(seconds=REQUEST_LIFETIME) < datetime.now()):
            data["term"] = self.term.to_json(nested=True)
        guesses = self.guesses.all()
        if not without_guess and len(guesses) > 0:
            data["guess"] = {
                "request": self.pk,
                "term": guesses[0].term.to_json(nested=True)
            }
        return data


class Guess(models.Model):

    CORRECT = "c"
    INCORRECT = "i"
    PARTIALLY_CORRECT = "pc"
    WE_DONT_KNOW = "wd"
    CORRECTNESS = (
        (CORRECT, "correct"),
        (INCORRECT, "incorrect"),
        (PARTIALLY_CORRECT, "partially correct"),
        (WE_DONT_KNOW, "we don't know"),
    )

    user = models.ForeignKey(User, related_name="guesses")
    request = models.ForeignKey(Request, related_name="guesses")
    term = models.ForeignKey(ExtendedTerm)
    timestamp = models.DateTimeField(auto_now_add=True)

    correct = models.CharField(max_length=2, choices=CORRECTNESS, null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    delay = models.IntegerField(null=True, blank=True)

    def to_json(self):
        data = {
            "request": self.request.to_json(nested=self.correct is not None, without_guess=True),
            "term": self.term.to_json(nested=True),
            "timestamp": self.timestamp,
        }
        if self.correct is not None:
            data["correct"] = self.correct
            data["points"] = self.points
            data["delay"] = self.delay
        return data

    def evaluate(self):
        if not self.term:
            return
        if not self.request.term:
            self.correct = self.WE_DONT_KNOW
            self.points = 30
            self.save()
            return

        self.delay = (self.timestamp - self.request.created).total_seconds()
        if self.term.name == self.request.term.name or self.request.term.name == self.term.name.split()[0]:
            self.correct = self.CORRECT
            coefficient = 1
        elif self.term.name.split()[0] == self.request.term.name.split()[0]:
            self.correct = self.PARTIALLY_CORRECT
            coefficient = 0.5
        else:
            self.correct = self.INCORRECT
            coefficient = 0
        self.points = coefficient * MAX_POINTS * max(0, 1 - self.delay / REQUEST_LIFETIME)
        self.save()
