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
import sys, platform, threading, socket, signal
py_ver = platform.python_version().split('.')[0]
print("Using Python v.", platform.python_version())

if len(sys.argv) != 2:
    print("Usage: server_YaChat.py <server_port>")
    sys.exit()

server_port = int(sys.argv[1])
    
class User:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = int(port)

userList = []
clientThreadList = []


def signal_handler(sig, frame):
    print("Killing {} client connections...".format(len(clientThreadList)))
    for connection in clientThreadList:
        connection.terminate = True
    
    tcpSocket.shutdown(socket.SHUT_RDWR)
    tcpSocket.close()
    print("Exiting")
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)



def userExists(userName):
    for user in userList:
        if user.name == userName:
            return user
    return False

def sendMessage(messageText):
    message = "{}\n".format(messageText)
    for user in userList:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            rcpt = (user.ip, user.port)
            sock.sendto(bytes(message, 'utf8'), rcpt)

def addUser(newUser):
    #Add newUser to the userList, then send UDP 'JOIN' message to all users in list
    if userExists(newUser) == False:
        userList.append(newUser)
        print("{} joined; {} users now".format(newUser.name, len(userList)))

        message = "JOIN {} {} {}".format(newUser.name, newUser.ip, newUser.port)
        sendMessage(message)
        
        
def delUser(rmUser):
    #Remove rmUser from userList, then send UDP 'EXIT' message to all users in the list
    user = userExists(rmUser)
    if user:
        userList.remove(user)
        print("{} left; {} users now".format(rmUser, len(userList)))
        message = "EXIT {}".format(rmUser)
        sendMessage(message)

def processMessage(self, message):
    message = message.strip()   #Remove the newline char
    msgArr = message.split(" ")
    if(len(msgArr) == 4 and msgArr[0] == 'HELO'):
        self.username = msgArr[1].strip()
        self.client_ip = msgArr[2].strip()
        self.client_port = msgArr[3].strip()
        newUser = User(self.username, self.client_ip, self.client_port)
        
        #Check userList for this username, send either ACPT or RJCT reply
        if userExists(newUser.name) == False:
            message = "ACPT "
            addUser(newUser)
            for index, user in enumerate(userList):
                message += "{} {} {}".format(user.name, user.ip, user.port)
                if index+1 < len(userList):
                    message += ":"
        else:
            message = "RJCT {}".format(newUser.name)
        
        message = "{}\n".format(message)
        self.conn.sendall(bytes(message, 'utf8'))
        
    elif (len(msgArr) == 1 and msgArr[0] == 'EXIT'):
        self.terminate = True
    
    
class clientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.client_ip = None
        self.client_port = None
        self.username = None
        self.terminate = False
        
    def run(self):
        while True:
            clientMsg = ""
            while '\n' not in clientMsg and self.terminate == False:
                msg = self.conn.recv(1024)
                clientMsg += msg.decode('utf8')

            if self.terminate == True:
                print("{}'s terminating!".format(self.username))
                delUser(self.username)
                self.conn.close()
                clientThreadList.remove(self)
                break
                
            processMessage(self, clientMsg)


# Server will be listening on TCP port for either HELO or EXIT messages
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpSocket:
    try:
        tcpSocket.bind(('0.0.0.0', server_port))
        tcpSocket.listen()
    except:
        print("TCP Bind/Listen to Port Failed")
        sys.exit()

    while True:
        conn, addr = tcpSocket.accept()
        newClient = clientThread(conn, addr)
        clientThreadList.append(newClient)
        newClient.start()
    
    
    
