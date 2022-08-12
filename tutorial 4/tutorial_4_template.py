import sys
import copy

from requests import delete

class SimpleGraph(object):
    def __init__(self, edge_list):
        self.vertex_dict = {}
        self.adj_list = []
        self.vertex_num = 0 
        self.edge_num  = 0 
        self.id_to_raw = dict()
        for [src, dst] in edge_list:
            self.add_edge(src, dst)

    def printGraph(self):
        print('+++++++vertex:', self.vertex_dict)
        print('+++++++adj:', self.adj_list)
        print('+++++++id_to_raw:', self.id_to_raw)

    def add_vertex(self, name):
        id = self.vertex_num
        self.vertex_dict[name] = id
        self.id_to_raw[id] = name
        self.vertex_num += 1
        self.adj_list.append(set())

    def getDegree(self, vertex):
        return  len(self.adj_list[self.vertex_dict[vertex]])

    def getLowestDegree(self):
        lowest = self.getDegree(self.vertex_num - 1)
        for name in self.vertex_dict:
            if lowest < self.getDegree(name):
                lowest = self.getDegree(name)
        return lowest

    def delete_edge(self, vertex1, vertex2):
        if vertex1 != vertex2:
            self.adj_list[self.vertex_dict[vertex1]].remove(vertex2)
            self.adj_list[self.vertex_dict[vertex2]].remove(vertex1)      
            self.edge_num = self.edge_num -1 
    
    def delete_vertex(self, vertex):
        
        self.adj_list.remove(vertex)
        del self.vertex_dict[vertex]


    def add_edge(self, vertex1, vertex2):
        if vertex1 != vertex2:
            if vertex1 not in self.vertex_dict.keys():
                self.add_vertex(vertex1)
            if vertex2 not in self.vertex_dict.keys():
                self.add_vertex(vertex2)
            self.adj_list[self.vertex_dict[vertex1]].add(vertex2)
            self.adj_list[self.vertex_dict[vertex2]].add(vertex1)
            self.edge_num = self.edge_num +1 

# Given K, this function computes the k-core. You need to complete this function
def onlineComputeKcore(K, G: SimpleGraph):
    kcore_vertices = [] 
    for name in G.vertex_dict:
        kcore_vertices.append(name)
    print(kcore_vertices, G.getLowestDegree())
    # insert your code here:
    while G.getLowestDegree() > K:
        print(G.vertex_num)
        for name in kcore_vertices:
            if G.getDegree(name) < K:
                kcore_vertices.remove(name)
                G.delete_vertex(name)
    #######################
    return kcore_vertices

# g1 is k-core subgraph, and V1 is the list of k-core vertices
# hint: density = number edges / number of vertices
def computeDensityForKcore(g1, V1):
    m = -1  # m represents the number of edges in k-core
    n = -1  # n represents the number of vertices in k-core
    d = -1  # d is a placeholder for k-core density
    # insert your code here:

    #######################
    print("|E({}-core)| = {}".format(K, m)) # show the number of edges in k-core
    print("|V({}-core)| = {}".format(K, n)) # show the number of vertices in k-core
    return d

# hint: you need to use the Union-Find class introduced in previous tutorials. 
def connectComponents(G):
    num_components = -1 # represents the number of connected component
    # insert your code here:

    ####################### 
    print("The number of connected components in the subgraph: " + str(num_components))


if __name__ == "__main__":
    # read in the graph data 
    edge_list_ = [[0, 1],
                [0, 4],
                [1, 3],
                [1, 4],
                [1, 6],
                [2, 3],
                [2, 6],
                [2, 8],
                [3, 4],
                [3, 6],
                [4, 5],
                [4, 6],
                [6, 7],
                [8, 9],
                [9, 10],
                [9, 12],
                [10, 11],
                [10, 12],
                [10, 13],
                [10, 14],
                [11, 12],
                [11, 13],
                [11, 14],
                [12, 13],
                [12, 14],
                [13, 14]]
    g1 = SimpleGraph(edge_list_)

    # query parameter K from command line
    # Note: If you are working in Colab, simply assign an number to K.
    K = int(sys.argv[1])

    # Exercise1: Computing k-core from the input graph
    V1 = onlineComputeKcore(K, g1)
    print("Online queried {}-core: {}".format(K,V1))

    # Exercise2: k-core based network analysis
    # (a) compute the graph density for k-core
    d = computeDensityForKcore(g1,V1)
    if d>0:
        print("density({}-core) = {}".format(K, d))
    else:
        print("{}-core does not exist.".format(K))

    # (b) explore the connectivity of k-core
    # Hint: use the Union-find class and the connectComponents() function introduced in Tutorial 2 for this task
    # Note that connectComponents() function counts the number of connected component of an input graph. 
    # It assumes that all vertices have positive degrees. Here you need to slightly modify the connectComponents() function. 
    ## call your modified function here
    connectComponents(g1)