import socket
import sys


HOST, PORT = "localhost", 9998

data = []
#data.append(b'')
data.append(b'\x00\x01')
data.append(b'\x80\x00')
#no of questions 
data.append(b'\x00\x01')
data.append(b'\x00\x00')
data.append(b'\x00\x00')
data.append(b'\x00\x00')
print(len(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    for i in (data):    
        sock.send(i)
    
    #map(lambda x:sock.send(bytes(data[x])),[i for i in range(len(data))])
    #map(lambda x:print(x),[i for i in range(len(data))])
    # Receive data from the server and shut down
    received = sock.recv(1024)

print("Sent:     {}".format(data))
print("Received: {}".format(received))

### to do form a dns packet dynamically 

def form_dns_packet(data):
    pass
