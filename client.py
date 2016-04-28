import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)

input_text = raw_input('Enter your command:')

isNotDone = True

while(isNotDone):
	input_string = input_text.split(' ', 1)
	if(input_string[0] == 'post'):
		s.send(input_text)
		print "Your message: " + input_string[1]
		isNotDone = False
	elif(input_string[0] == 'lookup'):
		s.send(input_text)
		print "MATTAFACKA"
		isNotDone = False
	elif(input_string[0] == 'sync'):
		s.send(input_text)
		print "sync with " + input_string[1]
		isNotDone = False
	else:
		input_text = raw_input('Wrong argument. Use post, lookup or sync? ')


s.close                     # Close the socket when done
