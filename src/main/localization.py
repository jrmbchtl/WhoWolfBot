import json
import os


def getLocalization(lang=None, primaryKey=None, no=None):
    if os.path.isfile("src/main/localization.json"):
        path = "src/main/localization.json"
    elif os.path.isfile("../localization.json"):
        path = "../localization.json"
    else:
        path = "../main/localization.json"
    with open(path, "r") as file:
        dc = json.load(file)
        if lang is None:
            return forceJoin(dc)
        elif primaryKey is None:
            return forceJoin(dc[lang])
        elif no is None:
            return forceJoin(dc[lang][primaryKey])
        else:
            return forceJoin(dc[lang][primaryKey][str(no)])


def forceJoin(dc):
    if isinstance(dc, list):
        return "".join(dc)
    elif isinstance(dc, dict):
        for d in dc:
            dc[d] = forceJoin(dc[d])
        return dc
    elif isinstance(dc, str):
        return dc
    else:
        raise ValueError("didn't expect " + str(dc) + " here")
