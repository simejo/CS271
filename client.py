import socket               # Import socket module


class Client(object):

	def __init__(self, port):
		self.s = socket.socket()         # Create a socket object
		#self.host = socket.gethostname() # Get local machine name
		self.port = port

	def start_connection(self, addr):
		s = self.s
		s.connect((addr, self.port))

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


		s.close

client = Client(12345)
client.start_connection(socket.gethostname()) #Input is the IP address to the one you want to connect to
