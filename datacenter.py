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
      self.threads = []

   def handle_post(self, message):
      self.timeTable.tick()
      time = self.timeTable.getTime()
      e = event.Event('post', message, time, self.node_id)
      self.log.input_in_log(e)
      self.dictionary.input_in_dict(time, message)
      print self.dictionary.toString()


   def handle_lookup(self, addr):
      """s = socket.socket()
      print addr
      s.connect(addr)
      print "sending = " +  self.dictionary.toString()
      s.send(self.dictionary.toString())
      s.close()
      #"""
      print "sending = " +  self.dictionary.toString()

      return self.dictionary.toString()


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

   """def check_message(self,message):
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
"""
   def initialize_connection(self):
      s = self.s
      s.bind((self.hostname, self.port_in))
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
      self.size = 1024
      self.server = server

   def run(self):
      print "INSIDE RUUUUNNNNNN"
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
            print "sending check_message = " +  dictionary

            self.c.send(dictionary)
         elif (input_string[0] == 'sync'):
            self.server.handle_sync(input_string[1])
         elif (input_string[0] == 'request_server_sync'):
            self.server.handle_request_server_sync()
         elif (input_string[0] == 'reply_server_sync_tt'):
            self.server.handle_time_table(input_string[1])
         elif (input_string[0] == 'reply_server_sync_log'):
            self.server.extend_log(input_string[1])
            self.server.update_dictionary()
            self.server.garbage_log(input_string[1])
      except Exception, e:
         print e
         print 'Something wrong happened. Server shutting down...'




server = datacenter(0, 12345, 10000)

def handler(signum, frame):
   try:
      print 'Ctrl+Z pressed'
   finally:
      server.close_connection()

signal.signal(signal.SIGTSTP, handler)

server.initialize_connection()