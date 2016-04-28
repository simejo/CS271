import socket               # Import socket module

class replicated_log(object):
	def __init__(self):
		self.log = {}

	def input_in_log(self, message, timestamp, process):
		self.log[timestamp+process] = message

	def lookup_log(self):
		for key, value in self.log.iteritems() :
			print key, value


s = socket.socket()         # Create a socket object
server_log = replicated_log() # Create replicated log
		

def handle_post(message):
	print "Handle Post .... " + str(message)


def handle_lookup():
	print 'Handle lookup ....'

def handle_sync(datacenter):
	print 'Handle sync with .... ' + str(datacenter)


#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
host = socket.gethostname() # Get local machine name
print "Server initialized. HOST: " + str(host) + " PORT:"
port = 12345                # Reserve a port for your service.
s.bind(('', port))        	# Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
	print "Server running..."
   	c, addr = s.accept()     # Establish connection with client.
   	print 'Got connection from', addr
   	c.send('Thank you for connecting')
   	message = c.recv(1024)


   	try:
   		input_string = message.split(' ', 1)
   		if (input_string[0] == "post"):
   			handle_post(input_string[1])
   		elif (input_string[0] == 'lookup'):
   			handle_lookup()
   		elif (input_string[0] == 'sync'):
   			handle_sync(input_string[1])
   	except Exception, e:
   		print 'Something wrong happend. Server shutting down...'
   		c.close()
   		break

   	if(message == 'post quit'):
   		c.close()
   		break
   	c.close()                # Close the connection




