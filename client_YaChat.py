#!/usr/bin/env python3

################################################################
# YaChat - Yet Another Chat Program
#
# Patrick Sigourney - pws482
# University of Texas at Austin - Spring 2019
# EE382N - Communication Networks; Dr. Yerraballi
#
# Usage: client.py <screen_name> <server_host> <server_port>
#
################################################################

import sys, platform, threading, queue,  socket

py_ver = platform.python_version().split('.')[0]
print("Using Python v.", platform.python_version())

if py_ver != '3':
	print("Requires Python3")
	sys.exit()

if len(sys.argv) != 4:
	print("Usage: client.py <screen_name> <server_host> <server_port>")
	sys.exit()

username = sys.argv[1]
server_host = sys.argv[2]
server_port = int(sys.argv[3])

# Message queue of items to be printed to the screen
printerQueue = queue.Queue()

# Messages received from a listener
recvQueue = queue.Queue()

# listenerThread will be passed a socket and will listen for incoming messages on that connection
# Received messages will be added to the recvQueue for processing
class listenerThread(threading.Thread):
	def __init__(self, netSock, port):
		threading.Thread.__init__(self)
		self.netSock = netSock
		self.listenPort = port

	def run(self):
		print("listenerThread started")
		while True:
			recvQueue.put(self.netSock.recvfrom(self.listenPort))
			


# printerThread will monitor the printerQueue and print any items it contains
class printerThread(threading.Thread):
	def __init__(self, dispQueue): 
		threading.Thread.__init__(self)
		self.displayQueue = dispQueue

	def run(self):
		print("printerThread started")
		while True:
			if not displayQueue.empty() :
				print(displayQueue.get())
				

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpSocket:

	udpListenerThread = listenerThread(udpSocket, 9876)
	udpListenerThread.start()


	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpSocket:

		try:
			tcpSocket.connect(server_host, server_port)
			my_ip = tcpSocket.getsockname()[0]
		except:
			print("TCP Connection to Server Failed")
			sys.exit()


