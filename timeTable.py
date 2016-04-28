# A class to represent the time table's held by each node
class TimeTable(object):

    def __init__(self, dim, node_id):
        self.dim = dim
        self.init_table()
        self.node_id = node_id

    def init_table(self):
        self.table = [[0]* self.dim for _ in range(self.dim)]
    
    # Update local row
    def tick(self):
        node = self.node_id
        print self.table[0][0]
    	self.table[node][node] +=1

    # Synchronize
    def synchronize_tt(self, t2):
    	for i in range(self.dim):
    		for j in range(self.dim):
    			self.table[i][j] = max(self.table[i][j], t2[i][j])

    def toString(self):
    	for i in range(self.dim):
    		print self.table[i]





