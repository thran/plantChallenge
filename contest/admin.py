from django.contrib import admin
from contest.models import Request, Guess


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("original_id", "created", "term", "images")

@admin.register(Guess)
class GuessAdmin(admin.ModelAdmin):
    list_display = ("user", "request", "term", "timestamp", "correct", "delay", "points")
