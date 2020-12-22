"""module implementing localization for the bot"""
import json
import os


def get_localization(lang=None, primary_key=None, index=None):
    """returns the quote for a specific key in a language"""
    if os.path.isfile("src/main/common/localization.json"):
        path = "src/main/common/localization.json"
    elif os.path.isfile("../common/localization.json"):
        path = "../common/localization.json"
    elif os.path.isfile("../main/common/localization.json"):
        path = "../main/common/localization.json"
    else:
        path = "localization.json"
    with open(path, "r") as file:
        dic = json.load(file)
        if lang is None:
            return force_join(dic)
        if primary_key is None:
            return force_join(dic[lang])
        if index is None:
            return force_join(dic[lang][primary_key])
        return force_join(dic[lang][primary_key][str(index)])


def force_join(dic):
    """joins list together into string, needed for multiline strings"""
    if isinstance(dic, list):
        return "".join(dic)
    if isinstance(dic, dict):
        for entry in dic:
            dic[entry] = force_join(dic[entry])
        return dic
    if isinstance(dic, str):
        return dic
    raise ValueError("didn't expect " + str(dic) + " here")
