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

myUsername = sys.argv[1]
server_host = sys.argv[2]
server_port = int(sys.argv[3])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpSocket:
		try:
			udpSocket.connect(('8.8.8.8', 80))
			my_ip = udpSocket.getsockname()[0]
		except:
			print("TCP Connection to Test Server Failed")
			sys.exit()


udpListenPort = 9989

class User:
	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = int(port)

		
# listenerThread will be passed a socket and will listen for incoming messages on that connection
# Received messages will be added to the recvQueue for processing
class listenerThread(threading.Thread):
	def __init__(self, netSock, port):
		threading.Thread.__init__(self)
		self.netSock = netSock
		self.listenPort = port

	def run(self):
		self.netSock.bind((my_ip, self.listenPort))
		while True:
			replyMsg = ""
			while '\n' not in replyMsg and self.netSock:
				reply = self.netSock.recv(4096)
				replyMsg += reply.decode('utf8')
			
			if replyMsg == 'DIE!\n':
				break
				
			parseUDPMsg(replyMsg)
			
			
def parseUDPMsg(message):
	messageArray = message.split(' ')
	if len(messageArray) < 2:
		print("Received invalid UDP message: ", message)
		return
	if messageArray[0] == 'MESG':
		messageText = ""
		for word in messageArray[2:]:
			messageText += word
		print("\n{}: {}".format(messageArray[1], messageText))
	elif messageArray[0] == 'JOIN':
		newUser = User(messageArray[1], messageArray[2], messageArray[3])
		if not knownUser(newUser.name, userList):
			userList.append(newUser)
	elif messageArray[0] == 'EXIT':
		removeUser(messageArray[1], userList)
	
def knownUser(username, userList):
	for user in userList:
		if username == user.name:
			return True
	return False
	
def removeUser(username, userList):
	for user in userList:
		if username == user.name:
			userList.remove(user)
			return

def sendMessage(messageText, userList):
	message = "MESG {} {}\n".format(myUsername, messageText)
	for user in userList:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
			rcpt = (user.ip, user.port)
			sock.sendto(bytes(message, 'utf8'), rcpt)
		
userList = []

# Fork off the UDP listener
# Establish TCP connection, send HELO, and recieve reply:
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpSocket:
	udpListenerThread = listenerThread(udpSocket, udpListenPort)
	udpListenerThread.start()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpSocket:
		try:
			tcpSocket.connect((server_host, server_port))

		except:
			print("TCP Connection to Server Failed")
			sys.exit()

		msg = 'HELO {} {} {}\n'.format(myUsername, my_ip, udpListenPort)
		tcpSocket.sendall(bytes(msg, 'utf8'))
		
		replyMsg = ""
		while '\n' not in replyMsg:
			reply = tcpSocket.recv(4096)
			replyMsg += reply.decode('utf8')
					  
		replyArray = replyMsg.split(" ")
		if len(replyArray) < 2:
			print("Received invalid TCP message: ", replyMsg)
			sys.exit()
		if replyArray[0] == 'RJCT':
			print("Username rejected")
			sys.exit()
		elif replyArray[0] == 'ACPT':
			removeACPT = replyMsg.split(" ", 1)
			userArray = removeACPT[1].split(":")
		
			for user in userArray:
				userParse = user.split(' ')
				newUser = User(userParse[0], userParse[1], userParse[2])
				if not knownUser(newUser.name, userList):
					userList.append(newUser)
		
		
		#Our connections are established, now accept user input from keyboard:
		while True:
			typing = input()
			parsedTyping = typing.split(" ", 1)
			if parsedTyping[0] == 'EXIT':
				tcpSocket.sendall(b'EXIT\n')
				
				#Kill off our UDP listener before we exit...
				with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
					rcpt = (my_ip, udpListenPort)
					sock.sendto(bytes('DIE!\n', 'utf8'), rcpt)		
					break
			else:
				sendMessage(typing, userList)

