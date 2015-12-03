from socket import *
from struct import *
from constants import *
import helpers, sender, receiver, packet


class Client:
	def __init__(self, serverAddr):
		self.remoteAddr = serverAddr

		self.SequenceNumber = helpers.getISN()
		self.lastack = None

		try:
			self.sockd = socket(AF_INET,SOCK_DGRAM)
		except:
			raise

		self.sockd.connect(serverAddr)
		self.address = self.sockd.getsockname()

		self.sender = sender.Sender(self.sockd)
		self.receiver = receiver.Receiver(self)

		# send SYN to server
		print("Initial sequence number: " + str(self.SequenceNumber))
		h = packet.Header(self.address[1], self.remoteAddr[1], self.SequenceNumber, 0, synf=1, ackf=0)

		
		self.sockd.send(h.pack())

		self.SYNSent()

	def SYNSent(self):
		# wait to receive SYN/ACK
		self.receiver.recv(self.SequenceNumber)
		
		self.established()

	def established(self):
		# receive data from server
		# when CLOSE/FIN is received, close
		f = open('out.mp4', 'w')

		while 1:
			try:
				self.receiver.recv(self.SequenceNumber)
			except:
				break
			self.receiver.passData(f)

		f.close()




conn = Client(('localhost',12000))
















