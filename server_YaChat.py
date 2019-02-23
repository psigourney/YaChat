#!/usr/bin/env python3

################################################################
# YaChat Server- Yet Another Chat Program
#
# Patrick Sigourney - pws482
# University of Texas at Austin - Spring 2019
# EE382N - Communication Networks; Dr. Yerraballi
#
# Usage: server.py <server_port>
#
################################################################
import sys, platform, threading, socket, queue
py_ver = platform.python_version().split('.')[0]
print("Using Python v.", platform.python_version())

if len(sys.argv) != 2:
	print("Usage: server_YaChat.py <server_port>")
	sys.exit()

server_port = int(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpSocket:
		try:
			udpSocket.connect(('8.8.8.8', 80))
			my_ip = udpSocket.getsockname()[0]
		except:
			print("TCP Connection to Test Server Failed")
			sys.exit()
    
class User:
	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = int(port)

userList = []
clientThreadList = []

def userExists(userList, userName):
    for user in userList:
        if user.name == userName:
            return user
    return False

def addUser(userList, newUser):
    #Add newUser to the userList, then send UDP 'JOIN' message to all users in list
    if !userExists(userList, newUser):
        userList.append(newUser)
        
        for user in userList:
            #Send UDP JOIN message to all

def delUser(userList, rmUser):
    #Remove rmUser from userList, then send UDP 'EXIT' message to all users in the list
    user = userExists(userList, rmUser)
    if user is not None:
        userList.remove(user)
        
        for user in userList:
            #Send UDP EXIT message to all
    

    
#Thread will accept as input the (conn, addr) pair returned by socket.accept()
class clientThread(threading.Thread):
	def __init__(self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.client_ip = None
        self.client_port = None
        self.username = None

    #We have a connection, should be getting a HELO
	def run(self):
		clientMsg = ""
		while '\n' not in clientMsg:
			msg = self.conn.recv(1024)
			clientMsg += msg.decode('utf8')
        clientMsg = clientMsg.strip()   #Remove the newline char
        clientMsgArray = clientMsg.split(" ")
        
        if(len(clientMsgArray) < 4 or clientMsgArray[0] != 'HELO'):
            print("clientMsgArray length < 4: ", clientMsg)
            break
        self.username = clientMsgArray[1].strip()
        self.client_ip = clientMsgArray[2].strip()
        self.client_port = clientMsgArray[3].strip()
        newUser = User(self.username, self.client_ip, self.client_port)
        #Check userList for this username, send either ACPT or RJCT reply
        #
        
        #Expecting EXIT message...
        clientMsg = ""
		while '\n' not in clientMsg:
			msg = self.conn.recv(1024)
			clientMsg += msg.decode('utf8')
        clientMsg = clientMsg.strip()   #Remove the newline char
        clientMsgArray = clientMsg.split(" ")
        
        if(len(clientMsgArray) < 1 or clientMsgArray[0] != 'EXIT'):
            print("clientMsgArray length < 1: ", clientMsg)
            break
        
        #Remove this user from userlist and exit thread
            
        
        


# Server will be listening on TCP port for either HELO or EXIT messages
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpSocket:
    try:
	    tcpSocket.bind(my_ip, server_port)
        tcpSocket.listen()
	except:
		print("TCP Bind/Listen to Port Failed")
		sys.exit()

    while True:
        conn, addr = tcpSocket.accept()
        newClient = clientThread(conn, addr)
        clientThreadList.append(newClient) #This may not be needed....
        newClient.start()
    
	tcpSocket.sendall(bytes(msg, 'utf8'))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    