############################################################################
# Do not edit this code cell.
############################################################################

from collections import deque
from math import inf

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
    def __init__(self, G, center, labels):
        self.G = G
        self.center = center
        self.prunedBFS(labels, 'out')
        self.prunedBFS(labels, 'in')
        
    def cover(self):
        return [self.ancs, self.desc]

    def labels(self):
        return self.labels

    def prunedBFS(self, labels, direction):
        # print('labels: {}'.format(labels))
        # print('number of labels: {}',format(self.num_labels(labels)))
        G = self.G
        src = self.center
        dist = {}
        q = deque()
        q.append(src)
        for v in G.vertex_dict:
            dist[v] = inf
        dist[src] = 0

        while len(q) != 0:
            u = q.popleft()
            if self.query_with_label(src, u, labels, direction) > dist[u]:
                labels[src][direction][u] = dist[u]

                if direction == 'out':
                    edges = G.adj_list_out[G.vertex_dict[u]]
                else:
                    edges = G.adj_list_in[G.vertex_dict[u]]

                for edge in edges:
                    v = edge[0]
                    v_dist = edge[1]
                    if dist[v] == inf:
                        q.append(v)
                    if dist[v] > dist[u] + v_dist:
                        dist[v] = dist[u] + v_dist
        return
                
    def query_with_label(self, source_vertex, target_vertex, labels, direction):
        reverse_direction = 'in' if direction == 'out' else 'out'
        out_label = {out_v for out_v in labels[source_vertex][direction]}
        in_label = {in_v for in_v in labels[target_vertex][reverse_direction]}

        if source_vertex in in_label:
            return labels[target_vertex][reverse_direction][source_vertex]
        if target_vertex in out_label:
            return labels[source_vertex][direction][target_vertex]
        dist = inf
        # print('path though middle nodes')
        for mid_v in out_label & in_label:
            curr_dist = labels[source_vertex][direction][mid_v] + labels[target_vertex][reverse_direction][mid_v]
            if curr_dist < dist:
                dist = curr_dist
        return dist
    
    def num_labels(self, labels):
        # print(labels)
        count = 0
        for v in labels:
            count += len(labels[v]['in'])
            count += len(labels[v]['out'])
        return count
        

class ShortestDistance(object):
    def __init__(self, G):
        self.G = G
        vertices = list(G.vertex_dict.keys())
        self.labels = {v: {'in': {}, 'out': {}}  for v in vertices}
        self.min_removed_edge = 0
        self.preprocess(G, self.labels)

    def preprocess(self, G: DirectedWeightedGraph, labels):
        labels = self.labels
        vertices = list(G.vertex_dict.keys())
        degrees = self.get_degrees(G)
        rounds = 0
        while len(degrees) != 0:
            rounds += 1
            print('rounds: {}'.format(rounds))
            curr_degree = -1
            curr_v = ''
            # print(self.get_num_path(uncovered_path))
            for v in degrees:
                next_degree = degrees[v]
                if next_degree >= curr_degree:
                    curr_degree = next_degree
                    curr_v = v
            if curr_v == '':
                break
            print('found curr_v: {}'.format(curr_v))
            degrees.pop(curr_v)
            # print('generating two hop cover...')
            curr_cover = TwoHopCover(G, curr_v, labels)
            # print('storing label...')
            # print('-----------')
            # print(curr_v)
            # print('start deletion')
            # print(self.labels)
            # print('cover: {}'.format(curr_cover.cover()))
            # print(uncovered_path)
            # print('removing edges...')
            # num_remove_edges = curr_cover.do_intersect(uncovered_path)

            # num_total_removed_edges += num_remove_edges
            # if num_remove_edges <= self.min_removed_edge:
                # print('stop. current edges: {}'.format(num_total_removed_edges))
                # break
            # print('reomve {} edges. current edges: {}'.format(num_remove_edges, num_total_removed_edges))
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
        # print('path though middle nodes')
        for mid_v in out_label & in_label:
            curr_dist = labels[source_vertex]['out'][mid_v] + labels[target_vertex]['in'][mid_v]
            if curr_dist < dist:
                dist = curr_dist
        return dist

    def get_degrees(self, G: DirectedWeightedGraph):
        vertices = list(G.vertex_dict.keys())
        d = {v: (len(G.adj_list_in[G.vertex_dict[v]]) + len(G.adj_list_out[G.vertex_dict[v]])) for v in vertices}
        return d

    # def form_reachable_path(self, curr_v, src, uncovered_path, visited):
    #     uncovered_path[src] = list(set(uncovered_path[src]) | set(uncovered_path[curr_v]))
    #     for v in uncovered_path[src]:
    #         if v not in visited:
    #             visited.add(v)
    #             self.form_reachable_path(v, src, uncovered_path, visited)
    #     return
