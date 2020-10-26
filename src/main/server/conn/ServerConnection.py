from queue import SimpleQueue
import socket
import json


class ServerConnection(object):
	def __init__(self, port=16384, host="127.0.0.1"):
		super(ServerConnection, self)
		self.port = port
		self.host = host
		self.recQueue = SimpleQueue()
		self.s = None
		self.conn = None
		self.addr = None

	def startServer(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setblocking(True)
		self.s.bind((self.host, self.port))
		self.s.listen(100000000)
		conn, self.addr = self.s.accept()
		self.s.close()
		self.s = conn

	def receiveJSON(self):
		fromServer = ""
		while True:
			data = self.s.recv(4096)
			if not data:
				fromServer = ""
				continue
			fromServer += data.decode('utf-8')
			print("Received: " + fromServer)
			try:
				json.loads(fromServer)
				return json.loads(fromServer)
			except ValueError:
				continue
		print("expected valid json but got " + fromServer)
		return self.receiveJSON()

	def sendJSON(self, dc):
		print("Sending: " + json.dumps(dc))
		self.s.send(json.dumps(dc).encode('utf-8'))

	def closeServer(self):
		self.s.close()
		self.conn.close()
