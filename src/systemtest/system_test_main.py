"""main module for running system tests"""
import json
import os
import time

from src.main.common.server_connection import ServerConnection
from src.systemtest.system_test_registration import SystemTestRegistration


class SystemTestMain:
    """client for system tests"""
    def __init__(self, rec_queue, send_queue):
        super()
        self.tests = []
        self.server_conn = ServerConnection(rec_queue, send_queue, "Systemtest")

    def main(self):
        """main method for system tests"""
        self.clean_up()
        SystemTestRegistration(self).register()
        for test in self.tests:
            print("\n\n##########################################################################")
            print("Running test " + test.get_name() + "\n\n")
            test.run()
            print("\n\n")
            time.sleep(2)
        self.clean_up()
        self.server_conn.send_json({"commandType": "close"})

    def register(self, test):
        """registers a test"""
        self.tests.append(test(self.server_conn))

    @staticmethod
    def clean_up():
        """cleans up all test files except crash test"""
        if not os.path.isdir("games"):
            return
        files = os.listdir("games/")
        for this_file in files:
            if os.path.isfile("games/" + this_file) and this_file.endswith(".game"):
                with open("games/" + this_file, "r") as file:
                    data = json.load(file)
                    if data["seed"] != 16384:
                        os.remove("games/" + this_file)
