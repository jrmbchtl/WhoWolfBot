class EditMode(object):
    WRITE = "write",
    EDIT = "edit",
    DELETE = "delete"


def createMessageEvent(target, text="", messageId=0, mode=EditMode.WRITE, highlight=False):
    dc = {"eventType": "message"}
    message = {"text": text, "messageId": messageId}
    dc["message"] = message
    if isinstance(mode, tuple):
        dc["mode"] = mode[0]
    else:
        dc["mode"] = mode
    dc["target"] = target
    dc["highlight"] = highlight

    return dc


def createChoiceFieldEvent(target, text="", options=None, messageId=0, mode=EditMode.WRITE,
                           highlight=False):
    if options is None:
        options = []
    dc = {"eventType": "choiceField"}
    choiceField = {"text": text, "options": options, "messageId": messageId}
    dc["choiceField"] = choiceField
    if isinstance(mode, tuple):
        dc["mode"] = mode[0]
    else:
        dc["mode"] = mode
    dc["target"] = target
    dc["highlight"] = highlight

    return dc
