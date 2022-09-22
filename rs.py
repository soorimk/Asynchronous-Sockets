import threading
import time
import random
import socket
import select
import sys


# Read command line aguments
rsListenPort = int(sys.argv[1])
ts1Hostname = sys.argv[2]
ts1ListenPort = int(sys.argv[3])
ts2Hostname = sys.argv[4]
ts2ListenPort = int(sys.argv[5])


# Create Socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()


# Connect to Client
server_binding_client = ('', rsListenPort)
ss.bind(server_binding_client)
ss.listen(1)
csockid, addr = ss.accept()
#print ("[S]: Got a connection request from a client at {}".format(addr))


# Connect to TS1
ts1_ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print("[C]: Ts1 Server socket created")
ts1_server_binding = (ts1Hostname, ts1ListenPort)
ts1_ss.connect(ts1_server_binding)


# Connect to TS2
ts2_ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print("[C]: Ts2 Server socket created")
ts2_server_binding = (ts2Hostname, ts2ListenPort)
ts2_ss.connect(ts2_server_binding)


while True: 

    # Receive data from Client
    msg = csockid.recv(200).decode()
    if not msg:
        break

    # Send data to Ts1 and Ts2
    ts1_ss.send(msg.encode('utf-8'))
    ts2_ss.send(msg.encode('utf-8'))

    # Receive data from Ts1 or Ts2
    # Using system call Select()
    readable, writable, exceptional = select.select([ts1_ss, ts2_ss], [], [], 5.0)
    ts_msg = msg + " - TIMED OUT"
    for i in readable: 
        if i is ts1_ss:
            ts_msg = ts1_ss.recv(200).decode()
        if i is ts2_ss:
            ts_msg = ts2_ss.recv(200).decode()
    
    # Send msg to Client
    csockid.send(ts_msg.encode('utf-8'))


# Close the server socket
ss.close()

exit()
