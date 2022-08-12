############################################################################
# Add any modules you want to use here~
############################################################################

from collections import namedtuple
import copy

path = namedtuple('path', ['src', 'dest', 'distance'])
early_stop = 30

class ShortestDistance(object):
    def __init__(self, G):
        self.G = G
        self.preprocess(G)

    def preprocess(self):
        G = collapse_G(G)
        split_G(G)

    def query(self, source_vertex, target_vertex):
        shortest_distance = 0
        return shortest_distance

def collapse_G(G):
    SCCs = get_strongly_connected_components()
    for SCC in SCCs:
        cycles = getCycles(G, SCC)
        v_hat = getDAG(cycles)
        for v in v_hat:
            add_two_hop_cover(v)
    G = remove_v(v_hat)
    return G

def split_G(G, v_sep)-> None:
    v_sep = find_separator()
    G_top, G_bot = separate_G(G, v_sep)
    for v in v_sep:
        add_two_hop_cover(v)

    if is_small(G_top):
        for v in G_top:
            add_two_hop_cover(v)
    else:
        split_G(G_top)

    if is_small(G_bot):
        for v in G_bot:
            add_two_hop_cover(v)
    else:
        split_G(G_bot)

def get_strongly_connected_components(G) ->list:
    SCCs = []
    visited = set()
    stack = []
    vertices = list(G.vertex_dict.keys())
    for v in vertices: 
        if v not in visited:
            DFS(G, [], v, visited, stack)
    print(stack)
    reverse = reverse_G(G)
    visited = set()
    while stack:
        v = stack.pop()
        if v not in visited:
            component = DFS(reverse, [], v, visited, [])
            SCCs.append(component)
    return SCCs

def getCycles(G, cycles):
    
def getDAG(cycles: list):
    current_cycle = cycles
    v_hat = set()
    if len(cycles) > early_stop:
        current_cycle = cycles[:early_stop]
        next_cycle = cycles[early_stop:]
        v_hat += getDAG(next_cycle)
    
    for vertices in cycles:
        v_total += set(vertices)
    v_appear_count = {}
    for v in v_total:
        for c in cycles

def add_two_hop_cover(v):
    pass
def remove_v(v_hat): 
    pass
def find_separator():
    pass
def separate_G(v_sep):
    pass
def is_small(G):
    pass

def DFS(G, traversal, vertex, visited, stack):
    visited.add(vertex)
    traversal.append(vertex)
    neighbors = G.adj_list_out[G.vertex_dict[vertex]]
    for out_edge in neighbors:
        v = out_edge[0]
        if v not in visited:
            DFS(G, traversal, v, visited, stack)
    stack.append(vertex)
    return traversal

def reverse_G(G):
    r_G = copy.deepcopy(G)
    temp = copy.deepcopy(r_G.adj_list_in)
    r_G.adj_list_in = r_G.adj_list_out
    r_G.adj_list_out = temp
    return r_G

############################################################################
# Do not edit this code cell.
############################################################################

class DirectedWeightedGraph(object):
    def __init__(self, edge_list):
        self.vertex_dict = {}
        self.adj_list_in = []
        self.adj_list_out = []
        self.vertex_num = 0
        for [src, dst, weight] in edge_list:
            self.add_edge(src, dst, weight)

    def add_vertex(self, name):
        id = self.vertex_num
        self.vertex_dict[name] = id
        self.vertex_num += 1
        self.adj_list_in.append(list())
        self.adj_list_out.append(list())

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.vertex_dict.keys():
            self.add_vertex(vertex1)
        if vertex2 not in self.vertex_dict.keys():
            self.add_vertex(vertex2)
        self.adj_list_out[self.vertex_dict[vertex1]].append([vertex2, weight])
        self.adj_list_in[self.vertex_dict[vertex2]].append([vertex1, weight])

    def print_G(self):
        print('vertex_dict:', self.vertex_dict)
        print('adj_list_in:', self.adj_list_in)
        print('adj_list_out:', self.adj_list_out)
        print('vertex_num:', self.vertex_num)