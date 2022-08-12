import time
import numpy as np
from q1 import *
from copy import copy
from itertools import permutations

if __name__ == "__main__":
    edges = []
    edges.append(['A', 'B', 4])
    edges.append(['A', 'C', 2])
    edges.append(['A', 'D', 3])
    edges.append(['B', 'D', 1])
    edges.append(['C', 'H', 2])
    edges.append(['D', 'F', 8])
    edges.append(['D', 'E', 2])
    edges.append(['E', 'C', 6])
    edges.append(['E', 'I', 2])
    edges.append(['F', 'C', 4])
    edges.append(['G', 'E', 3])
    edges.append(['H', 'E', 2])
    edges.append(['I', 'B', 5])
    edges.append(['I', 'G', 6])

    # edges = []
    # edges.append(['A', 'B', 3])
    # edges.append(['A', 'D', 3])
    # edges.append(['B', 'E', 2])
    # edges.append(['D', 'B', 10])
    # edges.append(['D', 'E', 14])
    G = DirectedWeightedGraph(edges)
    # G.print_G()
    a = ShortestDistance(G)
    # print('in: {}, out: {}'.format(a.labels_in, a.labels_out))
    # print(a.labels)
    # print('2 hop cover: {}'.format(TwoHopCover(G, 'E').cover()))
    print(a.query('A', 'E'))
    print(a.query('E', 'A'))
    print(a.query('D', 'B'))
    print(a.query('B', 'H'))
    print(a.query('C', 'E'))
    print(a.query('A', 'I'))
    print(a.query('G', 'C'))
    print(a.query('C', 'F'))


if __name__ == "__main__":

    print('\n##### Loading the dataset...')
    # edge_list = np.loadtxt('./COMP9312_datasets/cora.graph', dtype=int)
    # query_list = np.loadtxt('./COMP9312_datasets/cora.query', dtype=int)
    edge_list = np.loadtxt('./COMP9312_datasets/map_BJ_part.graph', dtype=int)
    query_list = np.loadtxt('./COMP9312_datasets/map_BJ_part.query', dtype=int)
    # edge_list = np.loadtxt('./COMP9312_datasets/map_NY_part.graph', dtype=int)
    # query_list = np.loadtxt('./COMP9312_datasets/map_NY_part.query', dtype=int)
    G = DirectedWeightedGraph(edge_list)
    # print('number of nodes: {}'.format(len(list(G.vertex_dict.keys()))))
    # print('number of edges: {}'.format(get_num_edges(G)))

    print('\n##### Start to preprocessing...')
    start_preprocessing = time.time()
    SD = ShortestDistance(G)
    end_preprocessing = time.time()
    print("preprocessing time: {}".format(end_preprocessing-start_preprocessing))

    # print(SD.labels)
    print('\n##### Test on the query ...')
    start_query = time.time()
    for i in range(query_list.shape[0]):
      distance = SD.query(query_list[i][0], query_list[i][1])
      print("the distance between {} and {} is: {}".format(query_list[i][0], query_list[i][1], distance))
    end_query = time.time()
    print("average  query time: {}".format((end_query-start_query)/query_list.shape[0]))


#     def do_intersect(self, non_covered_path):
#         for in_v in self.ancs:
#             ancs_path = (in_v, self.center)
#             # print('in ancs')
#             if ancs_path in non_covered_path:
#                 # print('deleted ancs: {}'.format(ancs_path))
#                 non_covered_path.remove(ancs_path)
#             for out_v in self.desc:
#                 two_hop_path = (in_v, out_v)
#                 if two_hop_path in non_covered_path:
#                     non_covered_path.remove(two_hop_path)
#         for out_v in self.desc:
#             desc_path = (self.center, out_v)
#             # print('in desc')
#             if desc_path in non_covered_path:
#                 # print('deleted desc: {}'.format(desc_path))
#                 non_covered_path.remove(desc_path)