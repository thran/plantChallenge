from collections import defaultdict
import csv
import json


lang = defaultdict(lambda: 0)
terms = []
HIT_LIMIT = 5
with open("source/flowers.csv") as f:
    f.readline()  # hack
    head = f.readline().split(",")
    for line in csv.reader(f.readlines()):
        data = dict(zip(head, line))
        if data["lang"] == "en" and int(data["counter"]) >= HIT_LIMIT:
            plant = {
                "id": str(data["id"]),
                "name-en": data["name"],
                "url": data["wikilink"],
            }
            terms.append(plant)

json.dump({"terms": terms}, open("terms.json", "w"), indent=4)