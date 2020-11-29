import datetime
import json
import logging
import os
import random
import time
from multiprocessing import Process

from telegram import Bot
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.error import RetryAfter
from telegram.error import TimedOut
from telegram.error import Unauthorized
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater

from src.main.localization import getLocalization as loc
from src.main.client.conn.ServerConnection import ServerConnection

illegalChars = ['.', '!', '#', '(', ')', '-', '=', '+', ']', '[', '{', '}', '>', '<', '|', '_', '*',
                '`', '~']

lang = "EN"


class TelegramClient(object):
    def __init__(self, recQueue, sendQueue):
        super(TelegramClient, self)
        self.sc: ServerConnection = ServerConnection(recQueue, sendQueue)
        with open('token.txt', 'r') as token_file:
            self.token = token_file.readline()
        self.token = self.token[0:46]
        self.bot = Bot(self.token)
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.spamDict = {}
        self.banList = self.getBanList()

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def run(self):
        p = Process(target=self.recProcess)
        p.start()
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('new', self.new))
        self.dispatcher.add_handler(CommandHandler('changelog', self.changelog))
        self.dispatcher.add_handler(CommandHandler('roles', self.roles))
        self.dispatcher.add_handler(CallbackQueryHandler(self.buttonHandler))
        self.updater.start_polling()
        self.updater.idle()

    def getBanList(self):
        if not os.path.isfile("banList.json"):
            with open("banList.json", "w") as file:
                json.dump([], file)
                return []
        with open("banList.json", "r") as file:
            return json.load(file)

    def writeBanList(self):
        with open("banList.json", "w") as file:
            print(self.banList)
            json.dump(self.banList, file)

    def isSpam(self, update):
        if update.callback_query is not None:
            userId = update.callback_query.from_user.id
            name = update.callback_query.from_user.first_name
            chatId = update.callback_query.message.chat_id
        else:
            userId = update.message.from_user.id
            name = update.message.from_user.first_name
            chatId = update.message.chat_id

        if userId in self.banList:
            return True

        now = datetime.datetime.now()
        if userId not in self.spamDict:
            self.spamDict[userId] = [now]
        else:
            self.spamDict[userId].append(now)
            i = 0
            while i < len(self.spamDict[userId]):
                if (now - self.spamDict[userId][i]).seconds > 60:
                    self.spamDict[userId].pop(i)
                else:
                    i += 1
            if len(self.spamDict[userId]) > 15:
                pre = loc(lang, "banSpamPre")
                post = loc(lang, "banSpamPost")
                text = pre + name + post
                dc = {
                    "eventType": "message", "message": {"text": text, "messageId": 0},
                    "target": chatId, "mode": "write", "gameId": 0, "lang": lang, "highlight": True
                }
                self.sendToBot(dc)
                self.banList.append(userId)
                self.writeBanList()
                return True
            elif len(self.spamDict[userId]) > 13:
                pre = loc(lang, "warnSpamPre")
                post = loc(lang, "warnSpamPost")
                text = pre + name + post
                dc = {
                    "eventType": "message", "message": {"text": text, "messageId": 0},
                    "target": chatId, "mode": "write", "gameId": 0, "lang": lang, "highlight": True
                }
                self.sendToBot(dc)
            return False

    def start(self, update, context):
        if self.isSpam(update):
            return
        self.botSendLoop(update.message.chat_id,
                         text=loc(lang, "welcome"),
                         parseMode=ParseMode.MARKDOWN_V2)

    def new(self, update, context):
        if self.isSpam(update):
            return
        fromId = update.message.from_user.id
        origin = update.message.chat_id
        seed = random.getrandbits(32)
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"seed": seed, "origin": origin},
                          "fromId": fromId})

    def changelog(self, update, context):
        if self.isSpam(update):
            return
        self.sc.sendJSON({"commandType": "changelog", "fromId": update.message.chat_id})

    def roles(self, update, context):
        if self.isSpam(update):
            return
        roleDict = loc(lang, "roles")
        roles = ""
        for index, role in enumerate(roleDict):
            roles += roleDict[role]
            if index + 1 < len(roleDict):
                roles += "\n"
        self.botSendLoop(update.message.chat_id, text=escapeText(roles),
                         parseMode=ParseMode.MARKDOWN_V2)

    def buttonHandler(self, update, context):
        print(update)
        if self.isSpam(update):
            return
        callbackData = update.callback_query.data
        gameId = int(callbackData.split("_")[1])
        name = update.callback_query.from_user.first_name
        playerId = update.callback_query.from_user.id
        if callbackData.startswith("register_"):
            self.sc.sendJSON({"commandType": "register", "register":
                {"name": name}, "fromId": playerId, "gameId": gameId})
        elif callbackData.startswith("add"):
            role = callbackData.split("_")[2]
            self.sc.sendJSON({"commandType": "add", "add": {"role": role}, "fromId": playerId,
                              "gameId": gameId})
        elif callbackData.startswith("remove"):
            role = callbackData.split("_")[2]
            self.sc.sendJSON({"commandType": "remove", "remove": {"role": role}, "fromId": playerId,
                              "gameId": gameId})
        elif callbackData.startswith("start_"):
            self.sc.sendJSON({"commandType": "startGame", "fromId": playerId, "gameId": gameId})
        elif callbackData.startswith("terminate_"):
            self.sc.sendJSON({"commandType": "terminate", "fromId": playerId, "gameId": gameId})
        else:
            choiceIndex = int(callbackData.split("_")[2])
            self.sc.sendJSON({"commandType": "reply", "reply":
                {"choiceIndex": choiceIndex}, "fromId": playerId, "gameId": gameId})

    def sendToBot(self, dc):
        messageId = dc[dc["eventType"]]["messageId"]
        target = dc["target"]
        mode = dc["mode"]
        if mode == "delete":
            self.botDeleteLoop(target, messageId)
            return messageId

        text = escapeText(dc[dc["eventType"]]["text"])
        gameId = dc["gameId"]
        if dc["highlight"]:
            text = "__" + text + "__"

        if dc["eventType"] == "message":
            replyMarkup = InlineKeyboardMarkup([])
        else:
            replyMarkup = InlineKeyboardMarkup(generateKeyboard(dc, gameId))

        if "parseMode" in dc[dc["eventType"]]:
            parseMode = dc["message"]["parseMode"]
        else:
            parseMode = ParseMode.MARKDOWN_V2

        if mode == "write":
            messageId = self.botSendLoop(target, text, replyMarkup, parseMode)
        elif mode == "edit":
            self.botEditLoop(target, text, messageId, replyMarkup, parseMode)
        return messageId

    def botSendLoop(self, chatId, text, replyMarkup=InlineKeyboardMarkup([]), parseMode=None):
        try:
            if parseMode is None:
                tmp = self.bot.send_message(chat_id=chatId, text=text, reply_markup=replyMarkup)
                return tmp.message_id
            else:
                tmp = self.bot.send_message(chat_id=chatId, text=text, reply_markup=replyMarkup,
                                            parse_mode=parseMode)
                return tmp.message_id
        except RetryAfter:
            time.sleep(15)
            self.botSendLoop(chatId, text, replyMarkup, parseMode)
        except TimedOut:
            time.sleep(15)
            self.botSendLoop(chatId, text, replyMarkup, parseMode)

    def botEditLoop(self, chatId, text, messageId, replyMarkup, parseMode=None):
        try:
            if parseMode is None:
                self.bot.edit_message_text(chat_id=chatId, message_id=messageId, text=text,
                                           reply_markup=replyMarkup)
            else:
                self.bot.edit_message_text(chat_id=chatId, message_id=messageId, text=text,
                                           reply_markup=replyMarkup, parse_mode=parseMode)
        except RetryAfter:
            time.sleep(15)
            self.botEditLoop(chatId, text, messageId, replyMarkup, parseMode)
        except TimedOut:
            time.sleep(15)
            self.botEditLoop(chatId, text, messageId, replyMarkup, parseMode)
        except BadRequest:
            return

    def botDeleteLoop(self, chatId, messageId):
        try:
            self.bot.delete_message(chat_id=chatId, message_id=messageId)
        except RetryAfter:
            time.sleep(15)
            self.botDeleteLoop(chatId, messageId)
        except TimedOut:
            time.sleep(15)
            self.botDeleteLoop(chatId, messageId)
        except BadRequest:
            return

    def recProcess(self):
        while True:
            rec = self.sc.receiveJSON()
            gameId = rec["gameId"]
            target = rec["target"]
            try:
                messageId = self.sendToBot(rec)
                self.sc.sendJSON({"commandType": "feedback", "feedback":
                                 {"success": 1, "messageId": messageId}, "fromId": target,
                                  "gameId": gameId})
            except Unauthorized:
                self.sc.sendJSON({"commandType": "feedback", "feedback":
                                 {"success": 0, "messageId": 0}, "fromId": target,
                                  "gameId": gameId})


def escapeText(text):
    newText = ""
    for c in text:
        if c in illegalChars:
            newText += "\\" + c
        else:
            newText += c
    return newText


def generateKeyboard(dc, gameId):
    keyboard = []
    lang = dc["lang"]
    if len(dc["choiceField"]["options"]) == 3 \
            and dc["choiceField"]["options"][0] == loc(lang, "join"):
        keyboard = [[InlineKeyboardButton(loc(lang, "join"),
                                          callback_data='register_' + str(gameId))],
                    [InlineKeyboardButton(loc(lang, "start"), callback_data='start_' + str(gameId)),
                     InlineKeyboardButton(loc(lang, "cancel"),
                                          callback_data='terminate_' + str(gameId))]]
    elif len(dc["choiceField"]["options"]) == 1 \
            and dc["choiceField"]["options"][0] == loc(lang, "cancel"):
        keyboard = [[InlineKeyboardButton(loc(lang, "cancel"),
                                          callback_data='terminate_' + str(gameId))]]
    elif dc["choiceField"]["text"] == loc(lang, "roleConfig"):
        for option in dc["choiceField"]["options"]:
            option = escapeText(option)
            if loc(lang, "removePre") in option and loc(lang, "removePost") in option:
                role = option[len(loc(lang, "removePre")):].split(" ")[0]
            else:
                role = option[len(loc(lang, "addPre")):].split(" ")[0]
            if option.endswith(loc(lang, "removePost")) \
                    and option.startswith(loc(lang, "removePre")):
                keyboard.append([InlineKeyboardButton(
                    option, callback_data="remove_" + str(gameId) + "_" + role)])
            else:
                keyboard.append([InlineKeyboardButton(
                    option, callback_data="add_" + str(gameId) + "_" + role)])
    else:
        for i, option in enumerate(dc["choiceField"]["options"]):
            option = escapeText(option)
            keyboard.append([InlineKeyboardButton(
                option, callback_data="reply_" + str(gameId) + "_" + str(i))])
    return keyboard
