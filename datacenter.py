import socket               # Import socket module
import timeTable
import event
import threading
import pickle
import log
import signal
import dictionary


class datacenter(object):
   def __init__(self, node_id, port_in, port_out):
      self.node_id = node_id
      self.s = socket.socket()
      self.timeTable = timeTable.TimeTable(2,node_id)
      self.hostname = socket.gethostname() # get local machine name
      self.port_in = port_in
      self.port_out = port_out
      self.addr = ''
      self.c = None
      self.log = log.Log()
      self.dictionary = dictionary.Dictionary(node_id)

   def handle_post(self, message):
      self.timeTable.tick()
      time = self.timeTable.getTime()
      e = event.Event('post', message, time, self.node_id)
      # Update log 
      self.log.input_in_log(e)
      # Update dictionary
      self.dictionary.input_in_dict(time, message)

      print 'The log: '
      print self.log.toString()
      print 'The time table: '
      print self.timeTable.toString()
      print 'The dictionary: '
      print self.dictionary.toString()


   def handle_lookup(self):
      print 'Handle lookup ....'
      s.send(self.dictionary.toString())


   def handle_sync(self, d2):
      #d2 is an IPaddress
      try:
         s = socket.socket()
         s.connect((d2, self.port_out))
         s.send("request_server_sync " + str(self.hostname))
         s.close()
         
      except Exception, e:
         print "Could not connect. " + str(e)
      print 'Handle sync with .... ' + str(d2)

   def handle_request_server_sync(self):
      time_table = pickle.dumps(self.timeTable)
      log = pickle.dumps(self.log)
      s = socket.socket()
      print self.addr
      s.connect((self.addr[0], self.port_out))
      s.send("reply_server_sync_tt " + time_table)
      s.close()
      s = socket.socket()
      s.connect((self.addr[0], self.port_out))
      s.send("reply_server_sync_log " + log)
      s.close()

   def handle_time_table(self, data):
      t2 = pickle.loads(data)
      self.timeTable.synchronize_tt(t2)
      print self.timeTable.toString()

   def update_dictionary(self):
      # NB: Watch up for DELETE events. May already have deleted the event, so we can not delete it
      for event in self.log.getLog():
         timestamp = event.getTime()
         nodeId = event.getNodeId()
         # This is for POST
         print "TIMESTAMP NODEID"
         print timestamp, nodeId
         if (timestamp, nodeId) not in self.dictionary.getDictionary():
            print "IN UPDATE: DO IT"
            self.dictionary.updateDictionary(timestamp, nodeId, event.getContent())


   def extend_log(self, log):
      l2 = pickle.loads(log)
      self.log.extendLog(l2)

   def garbage_log(self, log):
      for col in range(self.timeTable.getDim()):
         column = self.timeTable.getColumn(col)
         min_num = min(column)
         if(min_num > 0):
            self.log.delete_n_events_with_node_id_nid(min_num, col)

   def check_message(self,message):
      try:
         input_string = message.split(' ', 1)
         if (input_string[0] == "post"):
            self.handle_post(input_string[1])
         elif (input_string[0] == 'lookup'):
            self.handle_lookup()
         elif (input_string[0] == 'sync'):
            self.handle_sync(input_string[1])
         elif (input_string[0] == 'request_server_sync'):
            self.handle_request_server_sync()
         elif (input_string[0] == 'reply_server_sync_tt'):
            self.handle_time_table(input_string[1])
         elif (input_string[0] == 'reply_server_sync_log'):
            self.extend_log(input_string[1])
            self.update_dictionary()
            self.garbage_log(input_string[1])
      except Exception, e:
         print e
         print 'Something wrong happened. Server shutting down...'

   def initialize_connection(self):
      s = self.s
      s.bind((self.hostname, self.port_in))
      s.listen(5)
      while True:
         print "Server running... HOST: " + self.hostname
         c, addr = s.accept()     # Establish connection with client.
         self.addr = addr
         self.c = c
         print 'Got connection from', addr
         c.send('Thank you for connecting')
         message = c.recv(1024)
         self.check_message(message)
         c.close()                # Close the connection

   def close_connection(self):
      self.s.close()

server = datacenter(0, 12345, 10000)

def handler(signum, frame):
   try:
      print 'Ctrl+Z pressed'
   finally:
      server.close_connection()

signal.signal(signal.SIGTSTP, handler)

server.initialize_connection()