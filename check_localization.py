"""Checks if all localization elements are available in all languages"""
import json

FINE = True
with open("src/main/localization.json") as js:
    dc = json.load(js)
for lang in dc:
    if not isinstance(lang, str) or len(lang) != 2:
        FINE = False
        raise ValueError("Expected 2-Letter language code but got" + str(lang))
    keys = []
    for k in dc[lang]:
        keys.append(k)
    for la in dc:
        for k in keys:
            if k not in dc[la]:
                FINE = False
                raise ValueError("Found " + k + " in " + lang + " but not in " + la)
if FINE:
    print("everything is fine")
