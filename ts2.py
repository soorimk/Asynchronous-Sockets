import threading
import time
import random
import socket
import sys

# Read command line argument
ts2ListenPort = int(sys.argv[1])


# Create socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("[S]: TS2 created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()


# Connect to Server
server_binding = ('', ts2ListenPort)
ss.bind(server_binding)
ss.listen(1)
csockid, addr = ss.accept()


# Create DNS Table from PROJ2-DNSTS2.txt
DNS_table = {}
file1 = open('PROJ2-DNSTS2.txt', 'r')
Lines = file1.readlines()
for line in Lines:
    domain, ip, hold = line.split()
    DNS_table[domain] = ip
#print(DNS_table.items())


while True: 

    # Receive data from RS
    msg = csockid.recv(200).decode()
    msg = msg.strip()


    # No data received
    if not msg:
        break

    # Look for data in DNS Table
    for key in DNS_table.keys():
        if msg.lower() == key.lower():
            outputmsg = key + " " + DNS_table[key] + " A IN"
            csockid.send(outputmsg.encode('utf-8'))

file1.close()

# Close the server socket
ss.close()

exit()
