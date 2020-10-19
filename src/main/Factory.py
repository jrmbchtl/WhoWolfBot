from enum import Enum


class EditMode(Enum):
	WRITE = "write",
	EDIT = "edit",
	DELETE = "delete"


def createMessageEvent(target, text="", messageId=0, mode=EditMode.WRITE):
	dc = {}
	dc["eventType"] = "message"
	message = {}
	message["text"] = text
	message["messageId"] = messageId
	dc["message"] = message
	dc["mode"] = mode
	dc["target"] = target

	return dc


def createChoiceFieldEvent(target, text="", options=[], messageId=0, mode=EditMode.WRITE):
	dc = {}
	dc["eventType"] = "choiceField"
	choiceField = {}
	choiceField["text"] = text
	choiceField["options"] = options
	choiceField["messageId"] = messageId
	dc["choiceField"] = choiceField
	dc["mode"] = mode
	dc["target"] = target

	return dc
