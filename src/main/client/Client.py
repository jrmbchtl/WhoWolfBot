import logging
import time
from multiprocessing import Process

from telegram import Bot
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram.error import RetryAfter
from telegram.error import TimedOut
from telegram.error import Unauthorized
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater

from src.main.client.conn.ServerConnection import ServerConnection

illegalChars = ['.', '!', '#', '(', ')', '-', '=', '+', ']', '[', '{', '}', '>', '<', '|', '_', '*',
                '`', '~']


class Client(object):
    def __init__(self, serverConnection):
        super(Client, self)
        self.sc: ServerConnection = serverConnection
        with open('token.txt', 'r') as token_file:
            token = token_file.readline()
        self.bot = Bot(token)
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def run(self):
        p = Process(target=self.recProcess)
        p.start()
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('new', self.new))
        self.dispatcher.add_handler(CallbackQueryHandler(self.buttonHandler))
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, context):
        self.botSendLoop(update.message.chat_id,
                         text="Herzlich willkommen beim Werwolf\\-Bot\\!",
                         parseMode=ParseMode.MARKDOWN_V2)

    def new(self, update, context):
        senderId = update.message.from_user.id
        origin = update.message.chat_id
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"senderId": senderId},
                          "origin": origin})

    def buttonHandler(self, update, context):
        callbackData = update.callback_query.data
        gameId = int(callbackData.split("_")[1])
        name = update.callback_query.from_user.first_name
        playerId = update.callback_query.from_user.id
        origin = update.callback_query.message.chat.id
        if callbackData.startswith("register_"):
            self.sc.sendJSON({"commandType": "register", "register":
                {"name": name, "id": playerId}, "origin": origin, "gameId": gameId})
        elif callbackData.startswith("start_"):
            self.sc.sendJSON({"commandType": "startGame", "startGame":
                {"senderId": playerId}, "origin": origin, "gameId": gameId})
        elif callbackData.startswith("terminate_"):
            self.sc.sendJSON({"commandType": "terminate", "terminate":
                {"fromId": playerId}, "gameId": gameId})
        else:
            choiceIndex = int(callbackData.split("_")[2])
            self.sc.sendJSON({"commandType": "reply", "reply":
                {"fromId": playerId, "choiceIndex": choiceIndex},
                "origin": origin, "gameId": gameId})

    def sendToBot(self, dc):
        text = escapeText(dc[dc["eventType"]]["text"])
        messageId = dc[dc["eventType"]]["messageId"]
        target = dc["target"]
        mode = dc["mode"]
        gameId = dc["gameId"]

        if dc["eventType"] == "message":
            replyMarkup = InlineKeyboardMarkup([])
        else:
            keyboard = []
            if dc["choiceField"]["options"][0] == "Mitspielen/Aussteigen":
                keyboard = [[InlineKeyboardButton("Mitspielen/Aussteigen",
                                                  callback_data='register_' + str(gameId))],
                            [InlineKeyboardButton("Start", callback_data='start_' + str(gameId)),
                             InlineKeyboardButton("Abbrechen",
                                                  callback_data='terminate_' + str(gameId))]]
            else:
                for i, option in enumerate(dc["choiceField"]["options"]):
                    option = escapeText(option)
                    keyboard.append([InlineKeyboardButton(
                        option, callback_data="reply_" + str(gameId) + "_" + str(i))])
            replyMarkup = InlineKeyboardMarkup(keyboard)

        if "parseMode" in dc[dc["eventType"]]:
            parseMode = dc["message"]["parseMode"]
        else:
            parseMode = None

        if mode == "write":
            messageId = self.botSendLoop(target, text, replyMarkup, parseMode)
            print("messageId:" + str(messageId))
        elif mode == "edit":
            self.botEditLoop(target, text, messageId, replyMarkup, parseMode)
        elif mode == "delete":
            self.botDeleteLoop(target, messageId)
        print("messageId:" + str(messageId))
        return messageId

    def botSendLoop(self, chatId, text, replyMarkup=InlineKeyboardMarkup([]), parseMode=None):
        try:
            print("feedback from sending")
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

    def botDeleteLoop(self, chatId, messageId):
        try:
            print("deleting message" + str(messageId))
            self.bot.delete_message(chat_id=chatId, message_id=messageId)
        except RetryAfter:
            time.sleep(15)
            self.botDeleteLoop(chatId, messageId)
        except TimedOut:
            time.sleep(15)
            self.botDeleteLoop(chatId, messageId)

    def recProcess(self):
        while True:
            rec = self.sc.receiveJSON()
            gameId = rec["gameId"]
            try:
                messageId = self.sendToBot(rec)
                self.sc.sendJSON({"commandType": "feedback", "feedback":
                                 {"success": 1, "messageId": messageId}, "gameId": gameId})
            except Unauthorized:
                self.sc.sendJSON({"commandType": "feedback", "feedback":
                                 {"success": 0, "messageId": 0}, "gameId": gameId})


def escapeText(text):
    newText = ""
    for c in text:
        if c in illegalChars:
            newText += "\\" + c
        else:
            newText += c
    return newText
