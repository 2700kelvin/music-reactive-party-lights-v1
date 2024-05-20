#!/usr/bin/env python3
import signal
import sys
import socket                
from time import sleep
  
# next create a socket object 
s = socket.socket()          
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print("socket binded to ", port)
  
# put the socket into listening mode 
s.listen(5)      
print("socket is listening")
  
# a forever loop until we interrupt it or  
# an error occurs 
val = 125

while True: 
    # Establish connection with client. 
    c, addr = s.accept()      
    print('Got connection from', addr)
  
    # send a thank you message to the client.  
    # c.send('hello world\n'.encode())
    val = 0
    while(True):
        c.send(bytearray([val,0,0,0,val,0,0,0,val]))
        val += 1
        if(val > 255):
            val = 0
        # sleep(0.01)
  
    # Close the connection with the client 
    c.close() 
