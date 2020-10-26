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
			data = self.s.recv(4096)
			if not data:
				break
			fromServer += data.decode('utf-8')
			try:
				recJSON = json.loads(fromServer)
				print("Received: " + str(recJSON))
				return json.loads(recJSON)
			except ValueError:
				continue
		raise ValueError("Expected valid json but got :\n" + fromServer)

	def sendJSON(self, dc):
		print("Sending: " + json.dumps(dc))
		self.s.send(json.dumps(dc).encode('utf-8'))

	def receiveString(self):
		fromServer = ""
		while True:
			data = self.s.recv(4096)
			if not data:
				break
			fromServer += data.decode('utf-8')
			try:
				recJSON = json.loads(fromServer)
				print("Received: " + recJSON)
				return fromServer
			except ValueError:
				continue
		raise ValueError("Expected valid json but got :\n" + fromServer)

	def sendString(self, string):
		print("Sending: " + string)
		self.s.send(string.encode('utf-8'))

	def closeServer(self):
		self.s.close()
