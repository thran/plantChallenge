import json

dump = json.load(open("dump.json"))
fc = json.load(open("final/flashcards.json"))
fcs = json.load(open("final/flashcards-short.json"))
t = json.load(open("final/terms-clean.json"))
ts = json.load(open("final/terms-short.json"))


print len(dump["flashcards"]), len(dump["terms"]), len(dump["contexts"])
print len(fc["flashcards"]), len(fc["contexts"])
print len(fcs["flashcards"]), len(fcs["contexts"])
print len(t["terms"])
print len(ts["terms"])

diff = {"terms": [], "flashcards": [], "contexts": []}

terms_ids = map(lambda t: t["id"], dump["terms"])
for x in t["terms"] + ts["terms"]:
    if not x["id"] in terms_ids:
        print x
        diff["terms"].append(x)

fc_ids = map(lambda t: t["id"], dump["flashcards"])
for x in fc["flashcards"] + fcs["flashcards"]:
    if not x["id"] in fc_ids:
        print x
        diff["flashcards"].append(x)

fc_ids = map(lambda t: t["id"], dump["contexts"])
for x in fc["contexts"] + fcs["contexts"]:
    if not x["id"] in fc_ids:
        print x
        diff["contexts"].append(x)

json.dump(diff, open("diff.json", "w"), indent=4)
