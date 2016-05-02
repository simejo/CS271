
class Event(object):

	def __init__(self, op, content, time, node):
		self.op = op
		self.time = time
		self.node = node
		self.content = content
	
	def toString(self):
		return self.op, self.time, self.node, self.content