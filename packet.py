import struct
from constants import *

class Header:
	def __init__(self, sourcePort, destPort, sequence, ack, rwnd=0, ackf=1, synf=0, finf=0):
		self.sourcePort = sourcePort
		self.destPort = destPort

		self.sequencenumber = sequence
		self.ACKnum = ack
		self.rwnd = rwnd

		self.ACKf = ackf
		self.SYNf = synf
		self.FINf = finf
	

	def pack(self):
		return struct.pack(HFORMAT, self.sourcePort, self.destPort, self.sequencenumber,self.ACKnum,self.rwnd, self.ACKf,self.SYNf, self.FINf)

	def setRWND(self, rwnd):
		self.rwnd = rwnd

class Packet:
	def __init__(self, header, data=''):
		self.head = header.pack()
		self.data = data


	

