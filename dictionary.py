
class Dictionary(object):
	"""docstring for ClassName"""
	
	def __init__(self, node_id):
		self.dict = []
		self.node_id = node_id


	def input_in_dict(self, timestamp, content):
		self.dict.append("[(" + str(timestamp) + ", "  + str(self.node_id) + ")] : " + str(content))


	def updateDictionary(self, timestamp, node_id, content):
		self.dict.append("[(" + str(timestamp) + ", "  + str(node_id) + ")] : " + str(content))

	#Tuples are by default sorted by their first element (and if those are the same, then by the second, and so on), so no special key function is required
	
	def getDictionary(self):
		return self.dict

	def toString(self):
		holder = ""
		if len(self.dict) == 0:
			return "No posts yet..."
		for post in self.dict:
			holder += post + "\n"
		return holder



