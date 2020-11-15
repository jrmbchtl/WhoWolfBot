

class ServerConnection(object):
	def __init__(self, recQueue, sendQueue):
		super(ServerConnection, self)
		self.recQueue = recQueue
		self.sendQueue = sendQueue

	def receiveJSON(self):
		while self.recQueue.empty():
			pass
		data = self.recQueue.get()
		print("Client - Received: " + str(data))
		return data

	def sendJSON(self, dc):
		print("Client - Sending: " + str(dc))
		self.sendQueue.put(dc)
