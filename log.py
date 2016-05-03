class Log(object):
	def __init__(self):
		self.log = []

	def input_in_log(self, event):
		self.log.append(event)

	def lookup_log(self):
		print self.log
		
	def delete_in_log(self, event):
		self.log.remove(event)

	def delete_n_events_with_node_id_nid(n, nid):
		for event in self.log:
			if(event.getNodeId() == nid):
				delete_in_log(event)
				n -= 1
				if (n == 0):
					break


	def getLog(self):
		return self.log

	def extendLog(self, l2):
		self.log.extend(l2)

	def toString(self):
		holder = ""
		for event in self.log:
			holder += event.toString() + " :::: "
		return holder
