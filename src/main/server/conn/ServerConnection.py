from multiprocessing.queues import SimpleQueue


class ServerConnection(object):
	def __init__(self, recQueue, sendQueue: SimpleQueue):
		super(ServerConnection, self)
		self.recQueue = recQueue
		self.sendQueue = sendQueue

	def receiveJSON(self):
		while self.recQueue.empty():
			pass
		data = self.recQueue.get()
		print("Server - Received: " + str(data))
		return data

	def sendJSON(self, dc):
		print("Server - Sending: " + str(dc))
		self.sendQueue.put(dc)
