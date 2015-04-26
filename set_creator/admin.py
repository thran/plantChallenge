from django.contrib import admin
from set_creator.models import Set


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    pass
