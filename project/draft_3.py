############################################################################
# Do not edit this code cell.
############################################################################

from itertools import permutations
from math import inf
import copy

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


class TwoHopCover():
    def __init__(self, G, center) -> None:
        self.center = center
        self.desc = self.dijkstra(G, center, 'out')
        self.ancs = self.dijkstra(G, center, 'in')
        
    def cover(self):
        return [self.ancs, self.desc]

    def dijkstra(self, G: DirectedWeightedGraph, src, direction='out'):
        dist = {}
        prev = {}
        q = list(G.vertex_dict.keys())
        for v in G.vertex_dict:
            dist[v] = inf
            prev[v] = ''
        dist[src] = 0
        while len(q) != 0:
            u = self.get_u(q, dist)
            if dist[u] == inf:
                break
            q.remove(u)
            if direction == 'out':
                edges = G.adj_list_out[G.vertex_dict[u]]
            else:
                edges = G.adj_list_in[G.vertex_dict[u]]

            for edge in edges:
                v = edge[0]
                v_dist = edge[1]
                if dist[v] > dist[u] + v_dist:
                    dist[v] = dist[u] + v_dist
                    prev[v] = u
        for v in list(G.vertex_dict.keys()):
            if dist[v] == inf:
                dist.pop(v)
        dist.pop(src)
        return dist
                
    def get_u(self, q: list, dist: dict) ->str:
        nearest_v = q[0]
        nearest_dist = dist[q[0]]
        for v in q:
            if dist[v] < nearest_dist:
                nearest_v = v
                nearest_dist = dist[v]
        return nearest_v
    
    def cover_weight(self):
        return len(self.ancs) + len(self.desc)
    
    def intersect(self, vertices):
        non_covered_path = list(permutations(vertices, 2))
        num_total = len(non_covered_path)
        # print(self.center)
        # print(non_covered_path)
        self.do_intersect(non_covered_path)
        num_left = len(non_covered_path)
        return num_total - num_left
        
    def do_intersect(self, non_covered_path):
        for in_v in self.ancs:
            ancs_path = (in_v, self.center)
            # print('in ancs')
            if ancs_path in non_covered_path:
                # print('deleted ancs: {}'.format(ancs_path))
                non_covered_path.remove(ancs_path)
        for out_v in self.desc:
            desc_path = (self.center, out_v)
            # print('in desc')
            if desc_path in non_covered_path:
                # print('deleted desc: {}'.format(desc_path))
                non_covered_path.remove(desc_path)
            
    

class ShortestDistance(object):
    def __init__(self, G):
        self.G = G
        vertices = list(G.vertex_dict.keys())
        self.labels = {v: {'in': {}, 'out': {}}  for v in vertices}
        self.preprocess(G)


    def preprocess(self, G: DirectedWeightedGraph):
        vertices = list(G.vertex_dict.keys())
        stored = set()
        non_covered_path = list(permutations(vertices, 2))
        cover_list = {v: TwoHopCover(G, v) for v in vertices}
        curr_ratio = 0
        curr_v = ''
        while len(non_covered_path) != 0:
            # print(len(non_covered_path))
            for v in cover_list:
                next_ratio = cover_list[v].intersect(vertices) / cover_list[v].cover_weight()
                if next_ratio >= curr_ratio and v not in stored:
                    curr_ratio = next_ratio
                    curr_v = v
                    # print(v)
            
            self.store_labels(cover_list[curr_v])
            stored.add(curr_v)
            # print(curr_v)
            prev_non_covered_path = copy.copy(non_covered_path)
            # print('start deletion')
            cover_list[curr_v].do_intersect(non_covered_path)
            if prev_non_covered_path == non_covered_path:
                break
        return 

    def query(self, source_vertex, target_vertex):
        labels = self.labels
        out_label = {out_v for out_v in labels[source_vertex]['out']}
        in_label = {in_v for in_v in labels[target_vertex]['in']}

        if source_vertex in in_label:
            return labels[target_vertex]['in'][source_vertex]
        if target_vertex in out_label:
            return labels[source_vertex]['out'][target_vertex]

        dist = inf
        for mid_v in out_label & in_label:
            curr_dist = labels[source_vertex]['out'][mid_v] + labels[target_vertex]['in'][mid_v]
            if curr_dist < dist:
                dist = curr_dist
        return dist
    
    def store_labels(self, cover: TwoHopCover):
        v = cover.center
        labels = self.labels
        for in_v in cover.ancs:
            labels[in_v]['out'][v] = cover.ancs[in_v]
        for out_v in cover.desc:
            labels[out_v]['in'][v] = cover.desc[out_v]