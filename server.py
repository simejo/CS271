import socket               # Import socket module

def handle_post():
	print "POST"

def handle_lookup():
	print 'Handle lookup'

def handle_sync():
	print 'Handle sync'



s = socket.socket()         # Create a socket object
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname() # Get local machine name
print "Server initialized. HOST: " + str(host) + " PORT:"
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
	print "Server running..."
   	c, addr = s.accept()     # Establish connection with client.
   	print 'Got connection from', addr
   	c.send('Thank you for connecting')
   	message = c.recv(1024)


   	try:
   		input_string = message.split(' ', 1)
   		print 'TRY'
   		if (input_string[0] == "post"):
   			print 'POsdasdadssa'
   			handle_post()
   		elif (input_string[0] == 'lookup'):
   			handle_lookup()
   		elif (input_string[0] == 'sync'):
   			handle_sync()
   	except Exception, e:
   		print 'Something wrong happend. Server shutting down...'
   		c.close()
   		break

   	if(message == 'post quit'):
   		c.close()
   		break
   	c.close()                # Close the connection




