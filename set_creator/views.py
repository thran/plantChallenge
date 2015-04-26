from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
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
def remove_term(request, set_pk, term_pk):
    s = get_object_or_404(Set, pk=set_pk)
    s.terms.filter(pk=term_pk).delete()
    s.save()
    return redirect("set", set_pk)