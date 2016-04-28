import socket               # Import socket module
import timeTable
import event

class Replicated_log(object):
   def __init__(self):
      self.log = {}

   def input_in_log(self, message, timestamp, process):
      self.log[timestamp+process] = message

   def lookup_log(self):
      for key, value in self.log.iteritems() :
         print key, value

class ReplicatedDict(object):
   """docstring for ReplicatedDict"""
   def __init__(self):
      self.dict = {}
      


class datacenter(object):
   def __init__(self, node_id, port):
      self.node_id = node_id
      self.s = socket.socket()
      self.timeTable = timeTable.TimeTable(2,node_id)
      self.hostname = socket.gethostname() # get local machine name
      self.port = port

   def handle_post(self, message):
      print "Handle Post .... " + str(message)
      self.timeTable.tick()
      print self.timeTable.toString()

   def handle_lookup():
      print 'Handle lookup ....'

   def handle_sync(d2):
      print 'Handle sync with .... ' + str(d2)

   def initialize_connection(self):
      s = self.s
      s.bind((self.hostname, self.port))
      s.listen(5)
      while True:
         print "Server running..."
         c, addr = s.accept()     # Establish connection with client.
         print 'Got connection from', addr
         c.send('Thank you for connecting')
         message = c.recv(1024)


         try:
            input_string = message.split(' ', 1)
            if (input_string[0] == "post"):
               self.handle_post(input_string[1])
            elif (input_string[0] == 'lookup'):
               handle_lookup()
            elif (input_string[0] == 'sync'):
               handle_sync(input_string[1])
            elif (input_string[0] == 'quit'):
               s.close_connection()
               break
         except Exception, e:
            print e
            print 'Something wrong happend. Server shutting down...'
            c.close()
            break
         c.close()                # Close the connection

   def close_connection(self):
      self.s.close()

   def connect_to(self, addr):
      s = socket.socket()
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


server = datacenter(0,12345)
server.initialize_connection()
server.connect_to('')
