import socket               # Import socket module


class Client(object):

	def __init__(self, port):
		self.s = socket.socket()         # Create a socket object
		#self.host = socket.gethostname() # Get local machine name
		self.port = port

	def start_connection(self, addr):
		s = self.s
		s.connect((addr, self.port))
		print s.recv(1024)
		isNotDone = True
		while(isNotDone):
			input_text = raw_input('Enter your command:')
			input_string = input_text.split(' ', 1)
			if(input_string[0] == 'post'):
				s.send(input_text)
				print "Your message: " + input_string[1]
			elif(input_string[0] == 'lookup'):
				s.send(input_text)
				received_dictionary = s.recv(1024)
				print received_dictionary
			elif(input_string[0] == 'sync'):
				s.send(input_text)
				print "sync with " + input_string[1]
			elif(input_string[0] == 'close'):
				print "closing connection"
				isNotDone = False
			else:
				input_text = raw_input('Wrong argument. Use post, lookup or sync. "close" to close connection')


		s.close()

client = Client(12345)
client.start_connection('128.111.43.22') #Input is the IP address to the one you want to connect to
