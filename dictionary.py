
class Dictionary(object):
	"""docstring for ClassName"""
	
	def __init__(self, node_id):
		self.dict = []
		self.node_id = node_id


	def input_in_dict(self, timestamp, content):
		self.dict.append("[(" + str(timestamp) + ", "  + str(self.node_id) + ")] : " + str(content))


	def updateDictionary(self, timestamp, node_id, content):
		input_data = "[(" + str(timestamp) + ", "  + str(self.node_id) + ")] : " + str(content)
		if(input_data not in self.dict):
			self.dict.append("[(" + str(timestamp) + ", "  + str(self.node_id) + ")] : " + str(content))
	
	def getDictionary(self):
		return self.dict

	def toString(self):
		holder = ""
		if len(self.dict) == 0:
			return "No posts yet..."
		for post in self.dict:
			holder += post + "\n"
		return holder



