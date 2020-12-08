"""factory fro creating messages and choice fields"""
from enum import Enum


class EditMode(Enum):
    """class for esay comparision of message modes"""
    WRITE = "write"
    EDIT = "edit"
    DELETE = "delete"


def create_message_event(target, text="", message_id=0, config=None):
    """create a message dict"""
    if config is None:
        config = {}
    if "mode" in config:
        mode = config["mode"]
    else:
        mode = EditMode.WRITE
    if "highlight" in config:
        highlight = config["highlight"]
    else:
        highlight = False

    dic = {"eventType": "message"}
    message = {"text": text, "messageId": message_id}
    dic["message"] = message
    dic["mode"] = mode.value
    dic["target"] = target
    dic["highlight"] = highlight

    return dic


def create_choice_field_event(target, text="", options=None, message_id=0, config=None):
    """create a choice field dict"""
    if config is None:
        config = {}
    if "mode" in config:
        mode = config["mode"]
    else:
        mode = EditMode.WRITE
    if "highlight" in config:
        highlight = config["highlight"]
    else:
        highlight = False

    if options is None:
        options = []
    dic = {"eventType": "choiceField",
           "choiceField": {"text": text, "options": options, "messageId": message_id},
           "mode": mode.value, "target": target, "highlight": highlight}

    return dic
