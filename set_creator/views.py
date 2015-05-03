import json
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from proso_flashcards.models import Flashcard, Term
from practice.models import ExtendedTerm
from set_creator.models import Set


@staff_member_required
def set_list(request, *args):
    return render(request, 'sets/list.html', {
        "sets": Set.objects.all()
    })


@staff_member_required
def set_new(request):
    if request.method == "POST" and "name" in request.POST:
        s = Set.objects.create(name=request.POST["name"])
        return redirect("set", s.pk)


@staff_member_required
def set_detail(request, pk):
    return render(request, 'sets/detail.html', {
        "set": get_object_or_404(Set, pk=pk)
    })


@staff_member_required
def add_term(request, pk):
    s = get_object_or_404(Set, pk=pk)
    if request.method == "POST" and "term" in request.POST:
        t = get_object_or_404(ExtendedTerm, pk=int(request.POST["term"]))
        s.terms.add(t)
        s.save()
    return redirect("set", pk)


@staff_member_required
def add_terms(request, pk):
    set = get_object_or_404(Set, pk=pk)
    if request.method == "POST" and "pattern" in request.POST:
        pattern = request.POST["pattern"]
        pattern = pattern[0].upper() + pattern[1:].lower()
        for term in ExtendedTerm.objects.filter(name__startswith=pattern):
            set.terms.add(term)
            set.save()
    return redirect("set", pk)


@staff_member_required
def remove_term(request, set_pk, term_pk):
    s = get_object_or_404(Set, pk=set_pk)
    s.terms.filter(pk=term_pk).delete()
    s.save()
    return redirect("set", set_pk)

@staff_member_required
def term_detail(request, pk):
    flashcards = Flashcard.objects.filter(term_id=pk).order_by("identifier")
    for flashcard in flashcards:
        flashcard.images = json.loads(flashcard.context.content)
    return render(request, 'sets/term.html', {
        "flashcards": flashcards,
        "term": get_object_or_404(ExtendedTerm, pk=pk)
    })