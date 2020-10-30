from queue import SimpleQueue
import socket
import json


class ServerConnection(object):
	def __init__(self, port=32000, host="127.0.0.1"):
		super(ServerConnection, self)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = port
		self.host = host
		self.recQueue = SimpleQueue()

	def startServer(self):
		self.s.setblocking(True)
		self.s.connect((self.host, self.port))

	def receiveJSON(self):
		fromServer = ""
		while True:
			data = self.s.recv(1)
			if not data:
				fromServer = ""
				continue
			fromServer += data.decode('utf-8')
			try:
				json.loads(fromServer)
				print("Client - Received: " + fromServer)
				return json.loads(fromServer)
			except ValueError:
				continue
		print("expected valid json but got " + fromServer)
		return self.receiveJSON()

	def sendJSON(self, dc):
		print("Client - Sending: " + json.dumps(dc))
		self.s.send(json.dumps(dc).encode('utf-8'))

	def closeServer(self):
		self.s.close()
