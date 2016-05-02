class Log(object):
	def __init__(self):
		self.log = []

	def input_in_log(self, event):
		self.log.append(event)

	def lookup_log(self):
		print self.log
		
	def delete_in_log(self, event):
		self.log.remove(event)

	def toString(self):
		holder = ""
		for event in self.log:
			holder += event.toString() + " :::: "
		return holder
