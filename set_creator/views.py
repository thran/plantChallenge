import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from proso_flashcards.models import Flashcard, Term
from practice.models import ExtendedTerm
from set_creator.models import Set


@staff_member_required
def set_list(request, *args):
    return render(request, 'sets/list.html', {
        "sets": Set.objects.filter(for_daniel=False),
        "sets_for_daniel": Set.objects.filter(for_daniel=True),
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
    if request.method == "POST" and "pattern" in request.POST and len(request.POST["pattern"]) > 2:
        pattern = request.POST["pattern"]
        pattern = pattern[0].upper() + pattern[1:].lower()
        for term in ExtendedTerm.objects.filter(name__startswith=pattern):
            set.terms.add(term)
            set.save()
    return redirect("set", pk)


@staff_member_required
def remove_term(request, set_pk, term_pk):
    s = get_object_or_404(Set, pk=set_pk)
    term = get_object_or_404(Term, pk=term_pk)
    s.terms.remove(term)
    s.save()
    return redirect("set", set_pk)


@staff_member_required
def term_detail(request, pk):
    flashcards = Flashcard.objects.filter(term_id=pk).order_by("identifier")
    for flashcard in flashcards:
        try:
            flashcard.images = json.loads(flashcard.context.content)
        except ValueError:
            flashcard.json_error = "Invalid form of images json."
    return render(request, 'sets/term.html', {
        "flashcards": flashcards,
        "term": get_object_or_404(ExtendedTerm, pk=pk)
    })


@staff_member_required
def switch_for_daniel(request, pk):
    set = get_object_or_404(Set, pk=pk)
    set.for_daniel = not set.for_daniel
    set.save()
    return redirect("set_list")


@staff_member_required
def set_as_example(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    term = flashcard.get_term()
    term.example = flashcard
    term.save()
    return term_detail(request, term.pk)


@staff_member_required
def export_for_daniel(request):
    sets = {}
    for set in Set.objects.filter(for_daniel=True, active=True):
        images = []
        terms = []
        for term in set.terms.all():
            terms.append(term.name)
            for fc in term.flashcards.all().select_related("context"):
                images += json.loads(fc.context.content)
        sets[set.name] = {
            "images": images,
            "plants": terms,
        }

    return JsonResponse(sets)
