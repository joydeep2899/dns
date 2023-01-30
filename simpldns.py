from http.client import SWITCHING_PROTOCOLS
from re import S
import socketserver
from turtle import st
##########
'''

>>> a=bytearray([0x1,0x2])
>>> print(a)
bytearray(b'\x01\x02')
>>> a=bytearray([0xCf,0xDE])
>>> print(a)
bytearray(b'\xcf\xde')
>>> a[0]
207
>>> hex(a[0])
'0xcf'
>>> hex(a[1])
'0xde'
>>> a.append(0xAB)
>>> print(a)
bytearray(b'\xcf\xde\xab')
>>> hex(a[0:1])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'bytearray' object cannot be interpreted as an integer
>>> a[0:2]
bytearray(b'\xcf\xde')
>>> 
KeyboardInterrupt
>>> 
KeyboardInterrupt
print(int.from_bytes(b'\x00\x0d',byteorder='big'))
13

>>> 
'''

class MyTCPHandler(socketserver.BaseRequestHandler):
    #self.headers = {identification:0,flags:0,n_q:0,n_a:0,n_AA:0,n_ad:0}
    flags_data = {"QR":"","opcode":"","AA":"","TC":"","RD":"","RA":"","zero":"","rcode":""}
    flags_int = 0x0
    def process_data(self):
        for i in range(0,14,2):
          #print("step\n",i)
          txt="data : {data}, i : {index}"
         # print("data:",self.data[i-2:i],"\n")
          start_indx=i-2
          end_indx=i
          print(txt.format(data=self.data[start_indx:end_indx],index=i))
          if(start_indx==0):
            self.identification = self.data[start_indx:end_indx]
          if(start_indx ==2):
            self.flags = self.data[start_indx:end_indx]
            self.flags_int =int.from_bytes(self.flags,byteorder='big')
          if(start_indx==4):
            self.n_questions = self.data[start_indx:end_indx]
          if(start_indx ==6):
            self.n_answers = self.data[start_indx:end_indx]
          if(start_indx==8):
            self.n_authority = self.data[start_indx:end_indx]
          if(start_indx ==10):
            self.n_additional = self.data[start_indx:end_indx]
          
          self.flags_data["QR"]=(self.flags_int >>15 & 0x1)
          self.flags_data["opcode"]=(self.flags_int >>11 & 0xf)
          self.flags_data["AA"]=(self.flags_int >> 10 & 0x1)
          self.flags_data["TC"]=(self.flags_int >> 9 & 0x1)
          self.flags_data["RD"]=(self.flags_int >> 8 & 0x1)
          self.flags_data["RA"]=(self.flags_int >> 7 & 0x1)
          self.flags_data["zero"]= 0x0
          self.flags_data['rcode']=(self.flags_int & 0xf)
    def print(self):
        txt="identification : {}, flags : {}\n no of questions: {} , no of answer RR: {}\n".format(self.identification,self.flags,self.n_questions,self.n_answers)
        txt+="no of authority RR : {}, no of additional RR:{} \n".format(self.n_authority,self.n_additional)
        print(txt)

        print(self.flags_data)
    def handle(self):
        
        self.data =(self.request.recv(1024).strip())

        print("{} wrote:".format(self.client_address[0]))
        #a=self.data
        #print(type(self.data))
        #print(a[:3])
        self.process_data()
        self.print()
      

       # print(self.bytesdata[0])
        self.request.sendall(self.data)
        #for i in (self.data):    
        #  self.request.send(i)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever(poll_interval=2)
      
