from django.contrib import admin
from practice.models import ExtendedTerm, Request, ExtendedContext


@admin.register(ExtendedTerm)
class TermAdmin(admin.ModelAdmin):
    fields = ('name', 'url', 'interesting')

    def has_delete_permission(self, request, *args):
        return False


class RequestInline(admin.StackedInline):
    model = Request
    fields = ('term', 'active')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, *args):
        return False


@admin.register(ExtendedContext)
class FlashcardAdmin(admin.ModelAdmin):
    fields = ('fullname', 'content',)
    inlines = (RequestInline, )
    def has_delete_permission(self, request, *args):
        return False

