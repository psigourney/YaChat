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

print("{} is connecting to server {}:{}".format(username, server_host, server_port))

# Message queue of items to be printed to the screen
printerQueue = queue.Queue()

# listenerThread will be passed a socket connection and will listen for incoming messages on that connection
class listenerThread(threading.Thread):
	def __init__(self, threadID, connection):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.connection = connection

	def run(self):
		print('Thread {} started'.format(threadID))

# printerThread will monitor the printerQueue list and when it contains items, they will be printed
class printerThread(threading.Thread):
	def __init__(self, threadID, displayQueue): 
		threading.Thread.__init__(self)
		self.displayQueue = displayQueue

	def run(self):
		while true:
			if not displayQueue.empty() :
				print(displayQueue.get())
				



