from enum import Enum


class EditMode(Enum):
	WRITE = "write",
	EDIT = "edit",
	DELETE = "delete"


def createMessageEvent(target, text="", messageId=0, mode=EditMode.WRITE):
	dc = {"eventType": "message"}
	message = {"text": text, "messageId": messageId}
	dc["message"] = message
	dc["mode"] = mode
	dc["target"] = target

	return dc


def createChoiceFieldEvent(target, text="", options=None, messageId=0, mode=EditMode.WRITE):
	if options is None:
		options = []
	dc = {"eventType": "choiceField"}
	choiceField = {"text": text, "options": options, "messageId": messageId}
	dc["choiceField"] = choiceField
	dc["mode"] = mode
	dc["target"] = target

	return dc
