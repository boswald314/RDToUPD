from socket import *
from struct import *
from constants import *
import Queue
import helpers, constants, packet

class Receiver:
	def __init__(self, host):
		self.sock = host.sockd
		self.host = host
		self.port = self.sock.getsockname()[1]


		self.receivedData = Queue.Queue()


	def recv(self, sequence):
		#self.host.SequenceNumber = sequence
		msg, self.servAddr = self.sock.recvfrom(2048)
		header, payload = self.parseMsg(msg)
		self.sendAck(header, payload)

		
		if (header[FINF]==1):
			raise helpers.FINReceived
		
		

	def parseMsg(self, message):
		# separate header and payload
		head = message[:HEADERLENGTH]
		payload = message[HEADERLENGTH:]

		# return pair (header, data) where header is a list and data is raw
		header = helpers.unpackHeader(head)
		print header
		return (header, payload)

	def sendAck(self, header, payload):
		# send Ack packet for last received
		serverSeq = header[SEQNUM]

		outOfOrder = []
		
		if(header[SYNF] == 1):
			self.host.lastack = serverSeq + 1
			h = packet.Header(self.port, self.servAddr[1], self.host.SequenceNumber, self.host.lastack)
			self.sock.send(h.pack())
		elif(serverSeq == self.host.lastack):
			h = packet.Header(self.port, self.servAddr[1], self.host.SequenceNumber, self.host.lastack)
			self.sock.send(h.pack())
			self.receivedData.put(payload)
			self.host.lastack = serverSeq + len(payload)
		else:
			outOfOrder.append((header,payload))
		


		# must check if packets are in order
		# maintain list of packets received out of order?
		# when an in order packet is received, add to queue
		

	def passData(self, fout):
		try:
			fout.write(self.receivedData.get())
		except:
			pass










