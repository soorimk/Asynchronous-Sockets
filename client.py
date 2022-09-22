import threading
import time
import random
import socket
import sys


# Read command line arguments
rsHostname = sys.argv[1]
rsListenPort = int(sys.argv[2])


# Create Socket
try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()


# Connect to Server
server_binding = (rsHostname, rsListenPort)
cs.connect(server_binding)

file1 = open('PROJ2-HNS.txt', 'r')
file2 = open("RESOLVED.txt", "w")


while True:
 
    # Read lines from PROJ2-HNS.txt
    line = file1.readline()
 
    # End of File is reached
    if not line:
        break
    line = line.rstrip()
    cs.send((line).encode('utf-8'))

    # Receive data from the server
    data_from_rs="{}".format(cs.recv(200).decode('utf-8'))
    file2.write(data_from_rs + "\n")
    # print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))
 
file1.close()
file2.close()

# Close the client socket
cs.close()

exit()
