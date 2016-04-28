import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)

input = raw_input('Enter your command:')

isNotDone = True

while(isNotDone):
	input_string = input.split(' ', 1)
	if(input_string[0] == 'post'):
		s.send(input)
		print "Your message: " + input_string[1]
		isNotDone = False
	elif(input_string[0] == 'lookup'):
		s.send(input)
		print "MATTAFACKA"
		isNotDone = False
	elif(input_string[0] == 'sync'):
		s.send(input_string)
		print "sync with " + input_string[1]
		isNotDone = False
	else:
		input = raw_input('Wrong argument. Use post, lookup or sync? ')


s.close                     # Close the socket when done
