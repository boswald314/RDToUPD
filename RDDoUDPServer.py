from socket import *
from struct import *
from constants import *
import helpers, packet, sender, receiver
import time, threading


class Server:
	def __init__(self, address, port):
		'''
		Create instance of Server
			requires address and port to bind socket to
		performs passive open
		'''
		self.port = port
		self.lastack = None
		self.sockd = socket(AF_INET, SOCK_DGRAM)
		self.sockd.bind((address,port))
		print("bound socket")
		
		self.listen()

	def listen(self):
		synpacket, cliAddr = self.sockd.recvfrom(2048) 
		self.clientPort = cliAddr[1]
		head = helpers.unpackHeader(synpacket)
		#header = packet.Header(head)

		# check that received packet has SYN flag set
		print head
		assert head[SYNF] == 1, "Invalid packet -- not SYN"
		# set ACK number from client sequence number
		self.lastack = head[SEQNUM] + 1
		# connect with client 
		print("connect to " + str(cliAddr))
		self.sockd.connect(cliAddr)

		# instantiate sender/receiver
		self.sender = sender.Sender(self.sockd)
		self.receiver = receiver.Receiver(self)

		self.SYNReceived()

	def SYNReceived(self):
		self.SequenceNumber = helpers.getISN()
		# send SYN/ACK
		h = packet.Header(self.port, self.clientPort, self.SequenceNumber, self.lastack, ackf=0,synf=1)
		self.sender.send(h.pack())
		self.SequenceNumber = self.SequenceNumber + 1
		self.established()

	def established(self):
		# connection established, data transmission can occur
		# in theory, should listen for object requests
		# for now:

		t = threading.Thread(target=self.sendFile, args=("transfer.mp4",))
		print("starting")
		t.start()
		print("done")

		
		while 1:
			try:
				self.sender.transmit()
			except:
				break


		# send FIN
		h = packet.Header(self.port, self.clientPort, self.SequenceNumber, self.lastack, finf=1)
		self.sender.send(h.pack())
		self.close()



	def sendFile(self, f):
		# pass data to sender -- it is stored in send buffer
		with open(f,'rb') as fi:
			filecontents = fi.read()

		while len(filecontents):
			# get next chunk of data
			chunk = filecontents[:MSS]
			# then strip from remaining data
			filecontents = filecontents[len(chunk):]
			#print len(filecontents)


			# create header
			h = packet.Header(self.port, self.clientPort, self.SequenceNumber, self.lastack)
			# concatenate header and payload
			segment = h.pack() + chunk
			# add packet to buffer
			self.sender.addToBuffer(segment)
			# increment sequence number by number of bytes sent (and wrap sequence number if necessary)
			self.SequenceNumber = (self.SequenceNumber + len(chunk)) % SEQMAX

		print("file in buffer")

	def close(self):
		self.sockd.close()

serverinst = Server('localhost',12000)

serverinst.close()












