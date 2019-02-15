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
in
py_ver = platform.python_version().splial
print("Using Python v.", platform.python_version())
print("Exit with EXIT")

if py_ver != '3':
	print("Requires Python3")
	sys.exit()

if len(sys.argv) != 4:
	print("Usage: client.py <screen_name> <server_host> <server_port>")
	sys.exit()

myUsername = sys.argv[1]
server_host = sys.argv[2]
server_port = int(sys.argv[3])

# Make a test connection to find out my local IP address
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpSocket:
		try:
			udpSocket.connect(('8.8.8.8', 80))
			my_ip = udpSocket.getsockname()[0]
		except:
			print("TCP Connection to Test Server Failed")
			sys.exit()

udpListenPort = 0

class User:
	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = int(port)

		
# listenerThread will be passed a socket and will listen for incoming messages on that port
class listenerThread(threading.Thread):
	def __init__(self, netSock, port):
		threading.Thread.__init__(self)
		self.netSock = netSock
		self.port = port

	def run(self):
		self.netSock.bind((my_ip, 0))
		udpListenPort = udpSocket.getsockname()[1]
		self.port = udpListenPort
		while True:
			replyMsg = ""
			while '\n' not in replyMsg:
				reply = self.netSock.recv(1024)
				replyMsg += reply.decode('utf8')
			
			replyMsg = replyMsg.strip() #Strip newline char
			
			if replyMsg == 'DIE!':
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
			messageText += ' {}'.format(word)
		print("{}:{}".format(messageArray[1], messageText))
	elif messageArray[0] == 'JOIN':
		newUser = User(messageArray[1], messageArray[2], messageArray[3])
		if not knownUser(newUser.name, userList):
			userList.append(newUser)
			print("{} has joined the room.".format(messageArray[1]))
	elif messageArray[0] == 'EXIT':
		removeUser(messageArray[1], userList)
		print("{} has left the room.".format(messageArray[1]))
	
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
	udpListenerThread = listenerThread(udpSocket, 0)
	udpListenerThread.start()
		
	while udpListenerThread.port == 0:
		twiddleThumbs = True
		
	udpListenPort = udpListenerThread.port
		
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
			reply = tcpSocket.recv(1024)
			replyMsg += reply.decode('utf8')
					  
		replyArray = replyMsg.split(" ")
		if len(replyArray) < 2:
			print("Received invalid TCP message: ", replyMsg)
			sys.exit()
		elif replyArray[0] == 'RJCT':
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
			users = ""
			for user in userList:
				users += ' {}'.format(user.name)
			print("Current Users:{}".format(users))
		
		
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
