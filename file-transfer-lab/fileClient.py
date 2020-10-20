import socket
import sys
import re
#sys.path.append("./lib")       # for params
import params
from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), "server", "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

print("Sending the file")


file = input("type file to send : ")    #Gets file to send to server
textFile = bytes('recieve' +file, 'utf-8')  #file to bytes
framedSend(s, textFile, debug)  #sends using framed send
if (file):
    file_copy = open(file, 'r') #open file
    file_data = file_copy.read()    #save contents of file
    if len(file_data.encode('utf-8')) == 0: #if file is empty
        sys.exit(0)
    else:
        framedSend(s, file_data.encode(), debug)
        print("received:", framedReceive(s, debug))
else:
    print("file does not exist.")
    sys.exit(0)