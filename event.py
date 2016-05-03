
class Event(object):

	def __init__(self, op, content, time, node_id):
		self.op = op
		self.time = time
		self.node_id = node_id
		self.content = content
	
	def toString(self):
		return str(self.op) + ", " + str(self.time) + ", " + str(self.node_id) + ", " + str(self.content)

	def getNodeId(self):
		return self.node_id