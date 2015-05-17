# coding=utf-8
import json
import re


def parse_flower(flowerName):
    if ',' in flowerName:
        justName = flowerName.split(',')[0]
    else:
        justName = flowerName

    simpleName = parseNomenklature(flowerName, ['genus', 'species'])
    complexName = parseNomenklature(flowerName)

    if len(simpleName) > 0:
        simpleName = simpleName.lower()
        simpleName = simpleName[0].upper() + simpleName[1:]

    return simpleName, complexName


def parseNomenklature(flowerName, wantedFormat=None):
    attrs = ['genus', 'species', 'cultivar', 'variete', 'subsp', 'form']

    patterns = [
        u"^(?P<genus>([x×X] )?[a-zA-Z\-‒–—―‐]{2,}) +(?P<species>([x×X] )?[a-zA-Z\-‒–—―‐]{2,}) +(ssp.|subsp.) +(?P<subsp>[a-zA-Z\-‒–—―‐]{2,})( +(?P<cultivar>[’'‘‘’][a-z A-Z'\-‒–—―‐]{2,}['’‘‘’])|)( f. +(?P<form>[a-z A-Z'\-‒–—―‐]{2,})|)$",
        u"^(?P<genus>([x×X] )?[a-zA-Z\-‒–—―‐]{2,}) +(?P<species>([x×X] )?[a-zA-Z\-‒–—―‐]{2,}) +var(\.)? +(?P<variete>[a-zA-Z\-‒–—―‐]{2,})( +(?P<cultivar>[’'‘‘’][a-z A-Z'\-‒–—―‐]{2,}['’‘‘’])|)( f. +(?P<form>[a-z A-Z'\-‒–—―‐]{2,})|)$",
        u"^(?P<genus>([x×X] )?[a-zA-Z\-‒–—―‐]{2,}) +(?P<species>([x×X] )?[a-zA-Z\-‒–—―‐]{2,})( +(?P<cultivar>[’'‘‘’][a-z A-Z\-'‒–—―‐]{2,}['’‘‘’])|)( f. +(?P<form>[a-z A-Z'\-‒–—―‐]{2,})|)$",
        u"^(?P<genus>([x×X] )?[a-zA-Z\-‒–—―‐]{2,})( +(?P<cultivar>[’'‘‘’][a-z A-Z'-‒–—―‐]{2,}['’‘‘’])|)( f. +(?P<form>[a-z A-Z'\-‒–—―‐]{2,})|)$"
    ]

    structured = {}

    # find common name simple way
    flowerName = flowerName.strip()
    commonName = ''
    if ',' in flowerName:
        (flowerName, commonName) = flowerName.split(',', 1)
    flowerName = re.sub(" [A-Z]\. ", ' ', flowerName.strip())

    # stop at first match
    for p in patterns:
        match = re.search(p, flowerName)
        if match:
            for a in attrs:
                try:
                    structured[a] = match.group(a)
                    if not structured[a]:
                        structured[a] = ''
                except IndexError:
                    structured[a] = ''
            break

    if wantedFormat:
        resultFormat = ''
        for fu in wantedFormat:
            if not fu in structured:
                pass  # better then wire into eye
            else:
                resultFormat += ' %s' % structured[fu]

        return resultFormat.strip()

    if structured:
        structured['commonname'] = commonName.strip()

    return structured
