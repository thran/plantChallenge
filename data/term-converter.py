# coding=utf-8
from collections import defaultdict
import csv
import json
import re
import urllib2
from parser import parse_flower


def old():
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


def parse_flowers():
    urls = defaultdict(lambda: [])
    names = []
    flowers = json.load(open("source/flowers.json"))
    for flower in flowers:
        flower = flower["fields"]
        parsed = parse_flower(flower["name"])
        if parsed[0] != "" and parsed[1]["species"]:
            if len(parsed[1]["species"].split(" ")) > 1 or len(parsed[1]["genus"].split(" ")) > 1:
                continue
            names.append(parsed[0])
            urls[parsed[0]].append(flower["wikilink"])

    print len(flowers), len(names), len(set(names))

    return set(names), urls


def parse_plants():
    names = []
    plants = json.load(open("source/imported-plants.json"))
    for plant in plants:
        parsed = parse_flower(plant["pk"])
        if parsed[0] != "" and parsed[1]["species"]:
            names.append(parsed[0])

    # print len(plants), len(names), len(set(names))
    return set(names)


def find_urls(flowers, urls):
    for f in sorted(list(flowers)):
        try:
            url = "http://en.wikipedia.org/wiki/{}".format(f.replace(" ", "_"))
            wiki = urllib2.urlopen(url).read()
            print f, ", ", re.findall(r"<title>(.*)</title>", wiki)[0]
            urls[f] = [url]
        except urllib2.HTTPError:
            print f, len(urls[f])


def generate_terms():
    terms = []
    flowers, _ = parse_flowers()
    urls = json.load(open("urls.json"))
    for f in sorted(list(flowers)):
        if len(urls[f]) != 1:
            print f, urls[f]
        else:
            terms.append({
                "id": f,
                "name-en": f,
                "url": urls[f][0]
            })
    json.dump({"terms": terms}, open("terms.json", "w"), indent=4)


# generate_terms()
