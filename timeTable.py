# A class to represent the time table's held by each node
class TimeTable(object):

    def __init__(self, dim, node_id):
        self.dim = dim
        self.init_table()
        self.node_id = node_id
        self.timestamp = 0

    def init_table(self):
        self.table = [[0]* self.dim for _ in range(self.dim)]
    
    # Update local row
    def tick(self):
        node = self.node_id
        self.timestamp += 1
    	self.table[node][node] = self.timestamp
    
    def setTick(self, tickValue):
        self.timestamp = tickValue

    # Synchronize
    def synchronize_tt(self, t2):
        print "synchronize_tt()"
        max_timestamp = 0
        for i in range(self.dim):
            self.table[self.node_id][i] = max(t2.table[t2.node_id][i], self.table[self.node_id][i])
    	for i in range(self.dim):
    		for j in range(self.dim):
    			self.table[i][j] = max(self.table[i][j], t2.table[i][j])
                max_timestamp = max(self.table[i][j], max_timestamp)
                print "current max: " + str(max_timestamp)
        self.timestamp = max_timestamp
        print 'new timestamp: ', self.timestamp

    def toString(self):
    	for i in range(self.dim):
    		print self.table[i]

    def getColumn(self, c):
        return [row[c] for row in self.table]

    def getTimeTable(self):
        #return (self.node_id, self.table)
        return self

    def getDim(self):
        return self.dim

    def getNodeId(self):
        return self.node_id

    def getTime(self):
        return self.table[self.node_id][self.node_id]






