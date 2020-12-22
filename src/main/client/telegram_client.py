"""module for handling telegram communication"""
import datetime
import json
import logging
import os
import random
import re
import time
from multiprocessing import Process
from multiprocessing import Queue

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

from src.main.common import utils
from src.main.common.localization import get_localization as loc
from src.main.common.server_connection import ServerConnection

illegal_chars = ['.', '!', '#', '(', ')', '-', '=', '+', ']', '[', '{', '}', '>', '<', '|', '_',
                 '*', '`', '~']


class TelegramClient:
    """client for telegram communication"""

    def __init__(self, rec_queue, send_queue):
        super()
        self.server_conn: ServerConnection = ServerConnection(rec_queue, send_queue, "Telegram")
        with open('token.txt', 'r') as token_file:
            self.token = token_file.readline()
        self.token = self.token[0:46]
        self.bot = Bot(self.token)
        self.updater = Updater(self.token, use_context=True)
        self.spam_dict = {}
        self.ban_list = self.get_ban_list()
        self.config_queue = Queue()

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def run(self):
        """main thread for telegram client"""
        process = Process(target=self.rec_process)
        process.start()
        self.__dispatcher().add_handler(CommandHandler('start', self.start))
        self.__dispatcher().add_handler(CommandHandler('new', self.new))
        self.__dispatcher().add_handler(CommandHandler('changelog', self.changelog))
        self.__dispatcher().add_handler(CommandHandler('roles', self.roles))
        self.__dispatcher().add_handler(CommandHandler('join', self.join))
        self.__dispatcher().add_handler(CommandHandler('config', self.config))
        self.__dispatcher().add_handler(CallbackQueryHandler(self.button_handler))
        self.updater.start_polling()
        self.updater.idle()

    def __dispatcher(self):
        return self.updater.dispatcher

    @staticmethod
    def get_ban_list():
        """returns all banned accounts"""
        if not os.path.isfile("banList.json"):
            with open("banList.json", "w") as file:
                json.dump([], file)
                return []
        with open("banList.json", "r") as file:
            return json.load(file)

    def write_ban_list(self):
        """saves current ban list"""
        with open("banList.json", "w") as file:
            print(self.ban_list)
            json.dump(self.ban_list, file)

    def is_spam(self, update):
        """tests if someone is spamming"""
        if update.callback_query is not None:
            user_id = update.callback_query.from_user.id
            name = update.callback_query.from_user.first_name
            chat_id = update.callback_query.message.chat_id
        else:
            user_id = update.message.from_user.id
            name = update.message.from_user.first_name
            chat_id = update.message.chat_id

        if user_id in self.ban_list:
            return True

        now = datetime.datetime.now()
        lang = utils.get_lang(user_id)
        if user_id not in self.spam_dict:
            self.spam_dict[user_id] = [now]
        else:
            self.spam_dict[user_id].append(now)
            i = 0
            while i < len(self.spam_dict[user_id]):
                if (now - self.spam_dict[user_id][i]).seconds > 60:
                    self.spam_dict[user_id].pop(i)
                else:
                    i += 1
            if len(self.spam_dict[user_id]) > 15:
                pre = loc(lang, "banSpamPre")
                post = loc(lang, "banSpamPost")
                text = pre + name + post
                dic = {
                    "eventType": "message", "message": {"text": text, "messageId": 0},
                    "target": chat_id, "mode": "write", "gameId": 0, "lang": lang, "highlight": True
                }
                self.send_to_bot(dic)
                self.ban_list.append(user_id)
                self.write_ban_list()
                return True
            if len(self.spam_dict[user_id]) > 13:
                pre = loc(lang, "warnSpamPre")
                post = loc(lang, "warnSpamPost")
                text = pre + name + post
                dic = {
                    "eventType": "message", "message": {"text": text, "messageId": 0},
                    "target": chat_id, "mode": "write", "gameId": 0, "lang": lang, "highlight": True
                }
                self.send_to_bot(dic)
        return False

    def start(self, update, context):
        """handles start command"""
        check_context(context)
        if self.is_spam(update):
            return
        lang = utils.get_lang(update.message.from_user.id)
        self.bot_send_loop(update.message.chat_id,
                           text=loc(lang, "welcome"),
                           parse_mode=ParseMode.MARKDOWN_V2)

    def new(self, update, context):
        """handles new command"""
        check_context(context)
        if self.is_spam(update):
            return
        from_id = update.message.from_user.id
        origin = update.message.chat_id
        seed = random.getrandbits(32)
        self.server_conn.send_json(
            {"commandType": "newGame", "newGame": {"seed": seed, "origin": origin},
             "fromId": from_id})

    def changelog(self, update, context):
        """handles changelog command"""
        check_context(context)
        if self.is_spam(update):
            return
        self.server_conn.send_json({"commandType": "changelog", "fromId": update.message.chat_id})

    def roles(self, update, context):
        """handles roles command"""
        check_context(context)
        if self.is_spam(update):
            return
        lang = utils.get_lang(update.message.from_user.id)
        role_dict = loc(lang, "roles")
        roles = ""
        for index, role in enumerate(role_dict):
            roles += role_dict[role]
            if index + 1 < len(role_dict):
                roles += "\n"
        self.bot_send_loop(update.message.chat_id, text=escape_text(roles),
                           parse_mode=ParseMode.MARKDOWN_V2)

    def join(self, update, context):
        """function used to join a game in a different chat"""
        check_context(context)
        if self.is_spam(update):
            return
        from_id = update.message.from_user.id
        origin = update.message.chat_id
        name = update.message.from_user.first_name
        game_id = re.sub(r"\W", "", update.message.text[5:]).upper()
        lang = utils.get_lang(update.message.from_user.id)
        if from_id != origin:
            text = loc(lang, "sensitiveLeak")
            self.send_to_bot({'eventType': 'message', 'message': {
                'text': text, 'messageId': 0}, 'mode': 'write', 'target': origin,
                              'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        if len(game_id) != 6:
            text = loc(lang, "invalidIdPre") + game_id + loc(lang, "invalidIdPost")
            self.send_to_bot({'eventType': 'message', 'message': {
                'text': text, 'messageId': 0}, 'mode': 'write', 'target': origin,
                              'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        dic = {"commandType": "join", "register": {"name": name, "origin": origin},
               "fromId": from_id, "gameId": game_id}
        self.server_conn.send_json(dic)

    def config(self, update, context):
        """set the config"""
        check_context(context)
        if self.is_spam(update):
            return
        from_id = update.message.from_user.id
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        if from_id != chat_id:
            self.send_to_bot({'eventType': 'message', 'message': {
                'text': " ", 'messageId': message_id}, 'mode': 'delete', 'target': chat_id,
                              'highlight': False, 'gameId': "conf", 'lang': 'DE'})
            return
        process = Process(target=self.config_process, args=(update, self.config_queue,))
        process.start()

    def config_process(self, update, config_queue):
        """process for handling the config"""
        from_id = update.message.from_user.id
        lang = utils.get_lang(from_id)
        text = loc(lang, "choose_config")
        options = [loc(lang, "config_lang")]
        message_id = self.send_to_bot({"eventType": "choiceField", "choiceField": {
            "text": text, "options": options, "messageId": 0}, "target": from_id, "mode": "write",
                                       "gameId": "conf", "lang": "DE", "highlight": False})
        choice = self.config_get_option(config_queue, from_id)
        if choice == 0:
            text = loc(lang, "config_lang")
            options = []
            for lang in loc():
                options.append(lang)
            self.send_to_bot({"eventType": "choiceField", "choiceField": {
                "text": text, "options": options, "messageId": message_id}, "target": from_id,
                              "mode": "edit", "gameId": "conf", "lang": "DE", "highlight": False})
            utils.set_lang(from_id, options[self.config_get_option(config_queue, from_id)])
        self.send_to_bot({"eventType": "choiceField", "choiceField": {
            "text": text, "options": options, "messageId": message_id}, "target": from_id,
                          "mode": "delete", "gameId": "conf", "lang": "DE", "highlight": False})
        self.send_to_bot({'eventType': 'message', 'message': {
            'text': " ", 'messageId': update.message.message_id}, 'mode': 'delete',
                          'target': from_id, 'highlight': False, 'gameId': "conf", 'lang': 'DE'})

    @staticmethod
    def config_get_option(config_queue, from_id):
        """returns the next message sent by from_id"""
        while True:
            while config_queue.empty():
                pass
            dic = config_queue.get()
            if from_id in dic:
                return dic[from_id]
            config_queue.put(dic)
            time.sleep(1)

    def button_handler(self, update, context):
        """handles button presses"""
        check_context(context)
        if self.is_spam(update):
            return
        callback_data = update.callback_query.data
        game_id = callback_data.split("_")[1]
        name = update.callback_query.from_user.first_name
        player_id = update.callback_query.from_user.id
        if callback_data.startswith("register_"):
            self.server_conn.send_json({"commandType": "register", "register": {
                "name": name}, "fromId": player_id, "gameId": game_id})
        elif callback_data.startswith("add"):
            role = callback_data.split("_")[2]
            self.server_conn.send_json(
                {"commandType": "add", "add": {"role": role}, "fromId": player_id,
                 "gameId": game_id})
        elif callback_data.startswith("remove"):
            role = callback_data.split("_")[2]
            self.server_conn.send_json(
                {"commandType": "remove", "remove": {"role": role}, "fromId": player_id,
                 "gameId": game_id})
        elif callback_data.startswith("start_"):
            self.server_conn.send_json(
                {"commandType": "startGame", "fromId": player_id, "gameId": game_id})
        elif callback_data.startswith("terminate_"):
            self.server_conn.send_json(
                {"commandType": "terminate", "fromId": player_id, "gameId": game_id})
        elif callback_data.split("_")[1] == "conf":
            choice_index = int(callback_data.split("_")[2])
            self.config_queue.put({player_id: choice_index})
        else:
            choice_index = int(callback_data.split("_")[2])
            self.server_conn.send_json({"commandType": "reply", "reply": {
                "choiceIndex": choice_index}, "fromId": player_id, "gameId": game_id})

    def send_to_bot(self, dic):
        """send message to bot"""
        message_id = dic[dic["eventType"]]["messageId"]
        target = dic["target"]
        mode = dic["mode"]
        if mode == "delete":
            self.bot_delete_loop(target, message_id)
            return message_id

        text = escape_text(dic[dic["eventType"]]["text"])
        game_id = dic["gameId"]
        if dic["highlight"]:
            text = "__" + text + "__"

        if dic["eventType"] == "message":
            reply_markup = InlineKeyboardMarkup([])
        else:
            reply_markup = InlineKeyboardMarkup(generate_keyboard(dic, game_id))

        if "parseMode" in dic[dic["eventType"]]:
            parse_mode = dic["message"]["parseMode"]
        else:
            parse_mode = ParseMode.MARKDOWN_V2

        if mode == "write":
            message_id = self.bot_send_loop(target, text, reply_markup, parse_mode)
        elif mode == "edit":
            config = {"reply_markup": reply_markup, "parse_mode": parse_mode}
            message_id = self.bot_edit_loop(target, text, message_id, config)
        return message_id

    def bot_send_loop(self, chat_id, text, reply_markup=InlineKeyboardMarkup([]), parse_mode=None):
        """sends message till success"""
        try:
            if parse_mode is None:
                tmp = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
                return tmp.message_id
            tmp = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup,
                                        parse_mode=parse_mode)
            return tmp.message_id
        except RetryAfter:
            time.sleep(15)
            self.bot_send_loop(chat_id, text, reply_markup, parse_mode)
        except TimedOut:
            time.sleep(15)
            self.bot_send_loop(chat_id, text, reply_markup, parse_mode)

    def bot_edit_loop(self, chat_id, text, message_id, config):
        """edits message till success"""
        reply_markup = config["reply_markup"]
        parse_mode = config["parse_mode"]
        try:
            if parse_mode is None:
                self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                           reply_markup=reply_markup)
            else:
                self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                           reply_markup=reply_markup, parse_mode=parse_mode)
        except RetryAfter:
            time.sleep(15)
            self.bot_edit_loop(chat_id, text, message_id, config)
        except TimedOut:
            time.sleep(15)
            self.bot_edit_loop(chat_id, text, message_id, config)
        except BadRequest:
            pass
        return message_id

    def bot_delete_loop(self, chat_id, message_id):
        """deletes message till done"""
        try:
            self.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except RetryAfter:
            time.sleep(15)
            self.bot_delete_loop(chat_id, message_id)
        except TimedOut:
            time.sleep(15)
            self.bot_delete_loop(chat_id, message_id)
        except BadRequest:
            return

    def rec_process(self):
        """process for receiving from server"""
        while True:
            rec = self.server_conn.receive_json()
            game_id = rec["gameId"]
            target = rec["target"]
            try:
                if isinstance(target, list):
                    message_id = []
                    for index, target_id in enumerate(target):
                        rec2 = copy_dict(rec)
                        rec2["target"] = target_id
                        if isinstance(rec2[rec2["eventType"]]["messageId"], list) \
                                and index < len(rec2[rec2["eventType"]]["messageId"]):
                            rec2[rec2["eventType"]]["messageId"] = \
                                rec2[rec2["eventType"]]["messageId"][index]
                        elif isinstance(rec2[rec2["eventType"]]["messageId"], list) or index != 0:
                            rec2["mode"] = "write"
                        m_id = self.send_to_bot(rec2)
                        message_id.append(m_id)
                else:
                    message_id = self.send_to_bot(rec)
                self.server_conn.send_json({"commandType": "feedback", "feedback": {
                    "success": 1, "messageId": message_id}, "fromId": target, "gameId": game_id})
            except Unauthorized:
                self.server_conn.send_json({"commandType": "feedback", "feedback": {
                    "success": 0, "messageId": 0}, "fromId": target, "gameId": game_id})


def escape_text(text):
    """escapes text so it doesn't cause issues with markup"""
    new_text = ""
    for character in text:
        if character in illegal_chars:
            new_text += "\\" + character
        else:
            new_text += character
    return new_text


def generate_keyboard(dic, game_id):
    """generate a telegram keyboard"""
    keyboard = []
    lang = dic["lang"]
    if len(dic["choiceField"]["options"]) == 3 \
            and dic["choiceField"]["options"][0] == loc(lang, "join"):
        keyboard = [[InlineKeyboardButton(loc(lang, "join"),
                                          callback_data='register_' + str(game_id))],
                    [InlineKeyboardButton(loc(lang, "start"),
                                          callback_data='start_' + str(game_id)),
                     InlineKeyboardButton(loc(lang, "cancel"),
                                          callback_data='terminate_' + str(game_id))]]
    elif len(dic["choiceField"]["options"]) == 1 \
            and dic["choiceField"]["options"][0] == loc(lang, "cancel"):
        keyboard = [[InlineKeyboardButton(loc(lang, "cancel"),
                                          callback_data='terminate_' + str(game_id))]]
    elif dic["choiceField"]["text"] == loc(lang, "roleConfig"):
        for option in dic["choiceField"]["options"]:
            option = escape_text(option)
            if loc(lang, "removePre") in option and loc(lang, "removePost") in option:
                role = option[len(loc(lang, "removePre")):].split(" ")[0]
            else:
                role = option[len(loc(lang, "addPre")):].split(" ")[0]
            if option.endswith(loc(lang, "removePost")) \
                    and option.startswith(loc(lang, "removePre")):
                keyboard.append([InlineKeyboardButton(
                    option, callback_data="remove_" + str(game_id) + "_" + role)])
            else:
                keyboard.append([InlineKeyboardButton(
                    option, callback_data="add_" + str(game_id) + "_" + role)])
    else:
        for i, option in enumerate(dic["choiceField"]["options"]):
            option = escape_text(option)
            keyboard.append([InlineKeyboardButton(
                option, callback_data="reply_" + str(game_id) + "_" + str(i))])
    return keyboard


def check_context(context):
    """dummy function to make context used"""
    if context is None:
        raise ValueError("context should not be None")


def copy_dict(dic):
    """recursively copies a dict"""
    res = {}
    for key in dic:
        if isinstance(dic[key], dict):
            res[key] = copy_dict(dic[key])
        else:
            res[key] = dic[key]
    return res
