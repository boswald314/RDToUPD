import struct
import random
from constants import *
		
		

def packHeader(source,dest,seq,ack,ackf=1,synf=0,finf=0,rstf=0):
	''' header structure:
		---------32 bits------------
		--source port----dest port--
		------sequence number-------
		---------ack number---------

		-flags (4 bits)-
	'''
	header = struct.pack(HFORMAT, source, dest, seq, ack, ackf, synf, finf, rstf)
	return header


def unpackHeader(data):
	header = data[:HEADERLENGTH]
	header = struct.unpack(HFORMAT, header)
	return header

def getISN():
	return random.randrange(SEQMAX)

class FINReceived(Exception):
	pass
