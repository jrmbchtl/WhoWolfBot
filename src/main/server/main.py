"""main module for the werewolf-Bot"""
import argparse
import json
import os
import random
import string
import sys
from multiprocessing import Process
from multiprocessing import Queue

from src.main.client.telegram_client import TelegramClient
from src.main.common import utils
from src.main.common.localization import get_localization as loc
from src.main.common.server_connection import ServerConnection
from src.main.server import factory
from src.main.server.server import Server
from src.systemtest.system_test_main import SystemTestMain


class Main:
    """main class"""

    def __init__(self, enable_t_client=False, enable_sys_test_client=False):
        super()
        self.game_id = 1
        self.port = 32000
        self.games = {}
        self.from_server_queue = Queue()
        self.to_server_queue = Queue()
        self.server_conn = ServerConnection(self.to_server_queue, self.from_server_queue, "Server")
        self.client_list = []
        if enable_t_client:
            self.client_list.append(Process(target=start_telegram_client,
                                            args=(self.from_server_queue, self.to_server_queue,)))
            self.client_list[len(self.client_list) - 1].start()
        if enable_sys_test_client:
            self.client_list.append(Process(target=start_testing,
                                            args=(self.from_server_queue, self.to_server_queue,)))
            self.client_list[len(self.client_list) - 1].start()
            random.seed(42)

    def main(self, seed=42):
        """main loop"""
        self.restore_games(self.server_conn)
        self.game_id = self.get_next_game_id()
        try:
            while True:
                self.game_loop(seed)
        except KeyboardInterrupt:
            self.close_server()

    def game_loop(self, seed):
        """handling commands from  clients"""
        dic = self.server_conn.receive_json()
        command_type = dic["commandType"]
        if command_type == "newGame":
            if "seed" not in dic["newGame"]:
                dic["newGame"]["seed"] = seed
            self.init_game(self.game_id, self.server_conn, dic)
            self.game_id = self.get_next_game_id()
        elif command_type == "terminate":
            id_to_terminate = dic["gameId"]
            if id_to_terminate in self.games:
                self.safe_terminate(dic)
                self.clean_up()
        elif command_type == "close":
            self.close_server()
        elif command_type == "changelog":
            lang = utils.get_lang(dic["fromId"])
            send = factory.create_message_event(dic["fromId"], loc(lang, "changelog"))
            send["gameId"] = 0
            self.server_conn.send_json(send)
            self.server_conn.receive_json()
        elif dic["gameId"] in self.games:
            self.games[dic["gameId"]]["toProcessQueue"].put(dic)
        elif command_type == "join":
            lang = utils.get_lang(dic["fromId"])
            text = loc(lang, "noSuchGamePre") + dic["gameId"] + loc(lang, "noSuchGamePost")
            self.server_conn.send_json({'eventType': 'message', 'message': {
                'text': text, 'messageId': 0}, 'mode': 'write', 'target': dic["fromId"],
                                        'highlight': False, 'gameId': dic["gameId"],
                                        'lang': 'DE'})
        else:
            print("can't find a game with id " + str(dic["gameId"]))

    def close_server(self):
        """closes the server"""
        for game_id in self.games:
            self.games[game_id]["process"].kill()
        for client in self.client_list:
            client.kill()
        sys.exit(0)

    def safe_terminate(self, dic):
        """terminates all games"""
        game_id = dic["gameId"]
        if dic["fromId"] != self.games[game_id]["admin"]:
            return
        if game_id in self.games:
            self.games[game_id]["process"].kill()
            while not self.games[game_id]["deleteQueue"].empty():
                item = self.games[game_id]["deleteQueue"].get()
                message_id = item["messageId"]
                target = item["target"]
                dic = {"eventType": "message", "message": {"messageId": message_id},
                       "target": target, "mode": "delete", "gameId": game_id}
                self.server_conn.send_json(dic)
            self.clean_up()

    def restore_games(self, server_conn):
        """restores previously crashed games"""
        if not os.path.isdir("games/"):
            os.mkdir("games/")
        else:
            files = os.listdir("games/")
            for file in files:
                if not os.path.isfile("games/" + file):
                    continue
                if file.endswith(".game"):
                    try:
                        game_id = file.split(".")[0]
                    except ValueError:
                        continue
                    with open("games/" + file) as json_file:
                        data = json.load(json_file)
                    admin = data["admin"]
                    chat_id = data["chatId"]
                    seed = data["seed"]
                    number_sent = data["numberSent"]
                    rec_list = data["recList"]
                    dic = {"commandType": "newGame", "newGame": {
                        "numberSent": number_sent, "recList": rec_list, "origin": chat_id,
                        "seed": seed}, "fromId": admin}
                    self.init_game(game_id, server_conn, dic)

    def init_game(self, game_id, server_conn, dic):
        """initializes a game"""
        self.games[game_id] = {"toProcessQueue": Queue()}
        self.games[game_id]["admin"] = dic["fromId"]
        self.games[game_id]["deleteQueue"] = Queue()  # dicts with messageId, target
        self.games[game_id]["process"] = \
            Process(target=start_new_game,
                    args=(server_conn, dic, game_id, self.games[game_id]["toProcessQueue"],
                          self.games[game_id]["deleteQueue"],))
        self.games[game_id]["process"].start()

    def get_next_game_id(self):
        """returns next game_id available"""
        self.clean_up()
        while True:
            chars = string.ascii_uppercase
            for i in range(0, 10):
                chars += str(i)
            game_id = "".join(random.choice(chars) for i in range(6))
            if game_id not in self.games:
                return game_id

    def clean_up(self):
        """removes finished games"""
        rem_list = []
        for game_id in self.games:
            game: Process = self.games[game_id]["process"]
            if not game.is_alive():
                rem_list.append(game_id)
        for rem in rem_list:
            print("removing game " + str(rem))
            self.games.pop(rem, None)
            file = "games/" + str(rem) + ".game"
            if os.path.isfile(file):
                os.remove(file)


def start_new_game(server_conn, dic, game_id, game_queue, delete_queue):
    """starts a new game"""
    queues = {"game_queue": game_queue, "delete_queue": delete_queue}
    server = Server(server_conn, dic, queues, game_id)
    server.start()


def start_telegram_client(rec_queue, send_queue):
    """launches the telegram client"""
    t_client = TelegramClient(rec_queue, send_queue)
    t_client.run()


def start_testing(rec_queue, send_queue):
    """starts the system tests"""
    test_client = SystemTestMain(rec_queue, send_queue)
    test_client.main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-S", "--systemtest", help="run the system tests", action="store_true")
    parser.add_argument("-T", "--telegram", help="enables the Telegram Client", action="store_true")
    args = parser.parse_args()
    main = Main(enable_sys_test_client=args.systemtest, enable_t_client=args.telegram)
    main.main()
