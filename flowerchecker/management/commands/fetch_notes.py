from collections import Counter
import json
from optparse import make_option
from django.core.management import BaseCommand
from flowerchecker.models import Answer
from practice.models import ExtendedTerm

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--get',
            dest='get',
            action='store_true',
            default=False,
            help='fetch notes from FC'),
        make_option(
            '--apply',
            dest='apply',
            action='store_true',
            default=False,
            help='save notes to database'),
        make_option(
            '--filter',
            dest='filter',
            action='store_true',
            default=False,
            help='filter notes'),
    )

    def handle(self, *args, **options):
        if options["get"]:
            LLIMIT = 3
            result = {}

            for term in ExtendedTerm.objects.all():
                notes = list(Answer.objects.filter(answer__icontains=term.identifier).exclude(note="").values_list("note", flat=True))
                if len(notes) > 1 and max(Counter(notes).values()) >= LLIMIT:
                    self.stdout.write(term.name)
                    best = max(notes, key=notes.count)
                    self.stdout.write("   " + best)
                    result[term.name] = best

            json.dump(result, open("data/notes.json", "w"), indent=4)

        if options["apply"]:
            notes = json.load(open("data/notes-filtered.json"))
            for term, note in notes.items():
                term = ExtendedTerm.objects.get(name=term)
                if term.interesting == "" or term.interesting is None:
                    term.interesting = note
                    term.save()
                if term.interesting == note:
                    term.interesting = term.interesting[0].upper() + term.interesting[1:].lower()
                    term.save()

        if options["filter"]:
            notes = json.load(open("data/notes.json"))
            for term, note in notes.items():
                note = note.strip()
                if note.lower().startswith("or "):
                    del notes[term]
                    continue
                if "possibly" in note.lower():
                    del notes[term]
                    continue

                if note[-1] != ".":
                    note += "."
                notes[term] = note[0].uppper() + note[1:]

            json.dump(notes, open("data/notes-filtered.json", "w"), indent=4)


