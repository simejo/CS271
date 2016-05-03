import socket               # Import socket module
import timeTable
import event
import threading
import pickle
import log
import signal
import dictionary



class datacenter(object):
   def __init__(self, node_id, port, num_dc):
      self.node_id = node_id
      self.s = socket.socket()
      self.timeTable = timeTable.TimeTable(num_dc,node_id)
      self.hostname = socket.gethostname() # get local machine name
      self.port = port
      self.addr = ''
      self.c = None
      self.log = log.Log()
      self.dictionary = dictionary.Dictionary(node_id)
      self.threads = []

   def handle_post(self, message):
      self.timeTable.tick()
      time = self.timeTable.getTime()
      e = event.Event('post', message, time, self.node_id)
      self.log.input_in_log(e)
      self.dictionary.input_in_dict(time, message)
      print "------ Time Table ------"
      print self.timeTable.toString()
      print "------ Dictionary ------"
      print self.dictionary.toString()

   def handle_lookup(self, addr):
      print "------ Dictionary ------"
      print self.dictionary.toString()

      return self.dictionary.toString()


   def handle_sync(self, d2):
      #d2 is an IPaddress
      try:
         s = socket.socket()
         s.connect((d2, self.port))
         s.send("request_server_sync " + str(self.hostname))
         self.handle_request_server_sync(d2)
         s.close()
         
      except Exception, e:
         print "Could not connect. " + str(e)
      print 'Handle sync with .... ' + str(d2)

   def handle_request_server_sync(self,d1):
      time_table = pickle.dumps(self.timeTable)
      log = pickle.dumps(self.log)
      s = socket.socket()
      s.connect((d1.addr[0], self.port))
      s.send("reply_server_sync_tt " + time_table)
      s.close()
      s = socket.socket()
      s.connect((d1.addr[0], self.port))
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
         print timestamp, nodeId
         if (timestamp, nodeId) not in self.dictionary.getDictionary():
            self.dictionary.updateDictionary(timestamp, nodeId, event.getContent())

   def extend_log(self, log):
      l2 = pickle.loads(log)
      self.log.extendLog(l2)

   def garbage_log(self):
      print "----- Log before garbage -----"
      print self.log.toString()
      for col in range(self.timeTable.getDim()):
         column = self.timeTable.getColumn(col)
         min_num = min(column)
         if(min_num > 0):
            self.log.delete_n_events_with_node_id_nid(min_num, col)
      print "----- Log after garbage -----"
      print self.log.toString()

   def initialize_connection(self):
      s = self.s
      s.bind((self.hostname, self.port))
      s.listen(5)
      while True:
         print "Server running... HOST: " + self.hostname
         c, addr = s.accept()     # Establish connection with client.
         print 'Got connection from', addr       
         client = ClientHandler(c, addr, self)
         client.start()
         self.threads.append(client)

      self.s.close()
      for client in self.threads:
         client.join()

   def close_connection(self):
      self.s.close()

class ClientHandler(threading.Thread):
   def __init__(self, c, addr, server):
      threading.Thread.__init__(self)
      self.c = c
      self.addr = addr
      self.size = 1024*4
      self.server = server

   def run(self):
      self.c.send('Thank you for connecting')
      running = True
      while running:
         message = self.c.recv(self.size)
         if message:
            self.check_message(message)
         else:
            self.c.close()
            running = False


   def check_message(self,message):
      try:
         input_string = message.split(' ', 1)
         if (input_string[0] == "post"):
            self.server.handle_post(input_string[1])
         elif (input_string[0] == 'lookup'):
            dictionary = self.server.handle_lookup(self.addr)
            self.c.send(dictionary)
         elif (input_string[0] == 'sync'):
            self.server.handle_sync(input_string[1])
         elif (input_string[0] == 'request_server_sync'):
            self.server.handle_request_server_sync(self)
         elif (input_string[0] == 'reply_server_sync_tt'):
            self.server.handle_time_table(input_string[1])
         elif (input_string[0] == 'reply_server_sync_log'):
            self.server.extend_log(input_string[1])
            self.server.update_dictionary()
            self.server.garbage_log()
      except Exception, e:
         print e
         print 'Something wrong happened. Server shutting down...'



num_dc = raw_input('Number of datacenters: ')
server = datacenter(2, 12345, int(num_dc))


def handler(signum, frame):
   try:
      print 'Ctrl+Z pressed'
   finally:
      server.close_connection()

signal.signal(signal.SIGTSTP, handler)

server.initialize_connection()