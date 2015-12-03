from socket import *
from struct import *
from constants import *
import Queue
import helpers

_MSS = 1000

class Sender:
	"""docstring for Sender"""
	def __init__(self, sock):
		self.sock = sock

		# create send buffer
		self.buffer = Queue.Queue()

	def addToBuffer(self, packet):
		# add packet to buffer
		self.buffer.put(packet)

	def send(self, segment):
		# send packet which is passed in
		#print(helpers.unpackHeader(segment[:HEADERLENGTH]))
		self.sock.send(segment)

	def transmit(self):
		try:
			pack = self.buffer.get(timeout=10)
			self.send(pack)
		except:
			raise






		

