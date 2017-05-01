import copy
import itertools
import sys
import networkx as nx
import matplotlib.pyplot as plt
global total_connections


class Group:
    def __init__(self):
        self.members = []
        self.neighbors = list()
        self.a = float()
        
    def addMember(self, member, neighbors):
        self.members.append(member)
        for n in neighbors:
            self.neighbors.append(n)
        self.calculateA()
    
    def mergeTeam(self, team):        
        for m in team.members:
            self.members.append(m)
        for n in team.neighbors:
            self.neighbors.append(n)
        self.calculateA()
        return self

    def calculateA(self):
        self.a = float(len(self.neighbors)) / total_connections
                
    def __repr__(self):
        return '<Members: %r>' % (self.members)
 
    
def calculateModularityDifference(team_i, team_j):
    e_ij = calculateEIJ(team_i, team_j)
    return 2 * (e_ij - team_i.a * team_j.a)


def calculateEIJ(team_i, team_j):
    e_ij = float()
    for i_member in team_i.members:
        for j_neighbor in team_j.neighbors:
            if i_member == j_neighbor:
                e_ij += 1
    e_ij = e_ij / total_connections
    return e_ij


def findNeighbors(member, connections):
    neighbors = list()
    for connection in connections:
        if member in connection:
            temp = copy.deepcopy(connection)
            temp.remove(member)
            neighbors.append(temp[0])
    
    return neighbors

#The list of command line arguments passed to a Python script. argv[1] is the script name.
filename = sys.argv[1]
 
 #The Group argument, you can use argparse too to implement this.
if len(sys.argv) > 2:
	groups=sys.argv[2]
else:groups=2

total_connections = 0
teams = list()
connections = list()
unique_nodes = list()

G=nx.Graph()
G.add_nodes_from(unique_nodes)
with open(filename, 'r') as graph:
    for line in graph:
        pair = line.split()
        connections.append(pair)
        unique_nodes.append(pair[0])
        unique_nodes.append(pair[1])
        total_connections += 2
        # G.add_nodes_from(unique_nodes)
        G.add_edges_from(connections)



unique_nodes = list(set(unique_nodes))

for node in unique_nodes:
    temp = Group()
    temp.addMember(node, findNeighbors(node, connections))
    teams.append(temp)

q = float()
for t in teams:
    q += calculateEIJ(t, t) - t.a ** 2

while len(teams) > groups:

    #create all unique combinations between teams
    iterations = itertools.combinations(teams, 2)
    fpair = next(iterations)
    dqmax = calculateModularityDifference(fpair[0], fpair[1])
    pairmax = fpair[0], fpair[1]
    
    #manually iteration through the first pair
    for pair in iterations:
        dq = calculateModularityDifference(pair[0], pair[1])
        if dq > dqmax:
            dqmax = dq
            pairmax = pair[0], pair[1]
    teams.remove(pairmax[0])
    teams.remove(pairmax[1])
    new_team = pairmax[0].mergeTeam(pairmax[1])
    teams.append(new_team)
    #Q = Q + dqmax
    q += dqmax

output = list()
for team in teams:
    #sort team members
    output.append(sorted(map(int, team.members)))
output = sorted(output)
#draw and save graph for connections to png with filename : graph.png 
nx.draw(G)
plt.savefig("graph.png") # save as png
plt.show()

for team in output:
    print(team)
print("Q = %.4f" % q)