"""Module for exchanging data"""
from time import sleep


class ServerConnection:
    """Handles connection"""

    def __init__(self, rec_queue, send_queue, station):
        super()
        self.rec_queue = rec_queue
        self.send_queue = send_queue
        self.station = station

    def receive_json(self):
        """receive data"""
        while self.rec_queue.empty():
            pass
        data = self.rec_queue.get()
        print(self.station + " - Received: " + str(data))
        return data

    def send_json(self, dic):
        """send data"""
        if self.station == "Systemtest":
            sleep(0.1)
        print(self.station + " - Sending: " + str(dic))
        self.send_queue.put(dic)
