'''
Ryan Grayson
Google Foobar level 4.2: Escape Pods
06/13/22
'''

# Dinic's Algorithm - max network flow. credit https://www.geeksforgeeks.org/dinics-algorithm-maximum-flow/
class Edge:
    def __init__(self,v,flow,C,rev):
        self.v = v
        self.flow = flow
        self.C = C
        self.rev = rev
         
# Residual Graph
class Graph:
    def __init__(self,V):
        self.adj = [[] for i in range(V)]
        self.V = V
        self.level = [0 for i in range(V)]
         
    # add edge to the graph
    def addEdge(self,u,v,C):
       
        # Forward edge : 0 flow and C capacity
        a = Edge(v,0,C,len(self.adj[v]))
         
        # Back edge : 0 flow and 0 capacity
        b = Edge(u,0,0,len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)
         
    # Finds if more flow can be sent from s to t
    # Also assigns levels to nodes
    def BFS(self,s,t):
        for i in range(self.V):
            self.level[i] = -1
             
        # Level of source vertex
        self.level[s] = 0
         
        # Create a queue, enqueue source vertex
        # and mark source vertex as visited here
        # level[] array works as visited array also
        q = []
        q.append(s)
        while q:
            u = q.pop(0)
            for i in range(len(self.adj[u])):
                e = self.adj[u][i]
                if self.level[e.v] < 0 and e.flow < e.C:
                   
                    # Level of current vertex is
                    # level of parent + 1
                    self.level[e.v] = self.level[u]+1
                    q.append(e.v)
                     
        # If we can not reach to the sink we
        # return False else True
        return False if self.level[t]<0 else True
       
# A DFS based function to send flow after BFS has
# figured out that there is a possible flow and
# constructed levels. This functions called multiple
# times for a single call of BFS.
# flow : Current flow send by parent function call
# start[] : To keep track of next edge to be explored
#           start[i] stores count of edges explored
#           from i
# u : Current vertex
# t : Sink
    def sendFlow(self,u,flow,t,start):
        # Sink reached
        if u == t:
            return flow
 
        # Traverse all adjacent edges one -by -one
        while start[u] < len(self.adj[u]):
           
            # Pick next edge from adjacency list of u
            e = self.adj[u][start[u]]
            if self.level[e.v] == self.level[u]+1 and e.flow < e.C:
               
                # find minimum flow from u to t
                curr_flow = min(flow,e.C-e.flow)
                temp_flow = self.sendFlow(e.v,curr_flow,t,start)
                 
                # flow is greater than zero
                if temp_flow and temp_flow > 0:
                   
                    # add flow to current edge
                    e.flow += temp_flow
                     
                    # subtract flow from reverse edge
                    # of current edge
                    self.adj[e.v][e.rev].flow -= temp_flow
                    return temp_flow
            start[u] += 1
             
    # Returns maximum flow in graph
    def DinicMaxflow(self,s,t):
       
        # Corner case
        if s == t:
            return -1
           
        # Initialize result
        total = 0
         
        # Augument the flow while there is path
        # from source to sink
        while self.BFS(s,t) == True:
           
            # store how many edges are visited
            # from V { 0 to V }
            start = [0 for i in range(self.V+1)]
            while True:
                flow = self.sendFlow(s,float('inf'),t,start)
                if not flow:
                    break
                     
                # Add path flow to overall flow
                total += flow
                 
        # return maximum flow
        return total

def solution(entrances, exits, path):
    rooms = len(path)
    G = Graph(rooms + 2) # +2 for source and sink
    for i in range(rooms):
        for j in range(rooms):
            if path[i][j] > 0:
                G.addEdge(i, j, path[i][j])
    for e in entrances:
        G.addEdge(rooms, e, 2000000)
    for e in exits:
        G.addEdge(e, rooms+1, 2000000)

    return G.DinicMaxflow(rooms, rooms+1)


### TESTING ###

entrances1 = [0]
exits1 = [3]
path1 = [
    [0, 7, 0, 0], 
    [0, 0, 6, 0], 
    [0, 0, 0, 8], 
    [9, 0, 0, 0]
]
entrances2 = [0, 1]
exits2 = [4, 5]
path2 = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]
print
print(solution(entrances1, exits1, path1)) # expected 6
print
print(solution(entrances2, exits2, path2)) # expected 16
print