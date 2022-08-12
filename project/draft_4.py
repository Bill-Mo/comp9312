############################################################################
# Do not edit this code cell.
############################################################################

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
        self.max_edge = round(get_num_edges(G))
        self.desc = self.dijkstra(G, center, 'out')
        self.ancs = self.dijkstra(G, center, 'in')
        
    def cover(self):
        return [self.ancs, self.desc]

    def dijkstra(self, G: DirectedWeightedGraph, src, direction='out'):
        dist = {}
        edge_count = 0
        q = list(G.vertex_dict.keys())
        for v in G.vertex_dict:
            dist[v] = inf
        dist[src] = 0
        while len(q) != 0 and edge_count < self.max_edge:
            edge_count += 1
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
    
    # def intersect(self, vertices):
    #     uncovered_path = list(permutations(vertices, 2))
    #     num_total = self.get_num_path(uncovered_path)
    #     # print(self.center)
    #     # print(uncovered_path)
    #     self.do_intersect(uncovered_path)
    #     num_left = self.get_num_path(uncovered_path)
    #     return num_total - num_left
        
    def do_intersect(self, uncovered_path):
        count = 0
        # print(self.cover())
        # print(uncovered_path)
        center = self.center
        for in_v in self.ancs:
                # print('in ancs')
            try: 
                uncovered_path[in_v].remove(center)
                # print('deleted ancs: {}'.format((in_v, center)))
                count += 1
            except:
                pass
                
            # for out_v in self.desc:
            #     try:
            #         uncovered_path[in_v].remove(out_v)
            #         count += 1
            #     except ValueError:
            #         pass
        for out_v in self.desc:
            # print('in desc')
            try:
                uncovered_path[center].remove(out_v)
                # print('deleted desc: {}'.format((center, out_v)))
                count += 1
            except:
                pass
        return count
            
    

class ShortestDistance(object):
    def __init__(self, G):
        self.G = G
        vertices = list(G.vertex_dict.keys())
        self.labels = {v: {'in': {}, 'out': {}}  for v in vertices}
        self.min_removed_edge = 0
        self.preprocess(G)



    def preprocess(self, G: DirectedWeightedGraph):
        vertices = list(G.vertex_dict.keys())
        degrees = self.get_degrees(G)
        # uncovered_path = list(permutations(vertices, 2))
        uncovered_path = {v: copy.copy(vertices) for v in vertices}
        # print(degrees)
        # for v in vertices:
        #     self.form_reachable_path(v, v, uncovered_path, set())
        for v in vertices: 
            # print('before: {}'.format(uncovered_path[v]))
            uncovered_path[v].remove(v) 
            # print('after: {}'.format(uncovered_path[v]))
        rounds = 0
        num_total_removed_edges = 0
        print('removed edge number: {}'.format(num_total_removed_edges))
        while self.get_num_path(uncovered_path) >= 0:
            rounds += 1
            print('rounds: {}'.format(rounds))
            curr_degree = 0
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
            curr_cover = TwoHopCover(G, curr_v)
            # print('storing label...')
            self.store_labels(curr_cover)
            # print('-----------')
            # print(curr_v)
            # print('start deletion')
            # print(self.labels)
            # print('cover: {}'.format(curr_cover.cover()))
            # print(uncovered_path)
            # print('removing edges...')
            num_remove_edges = curr_cover.do_intersect(uncovered_path)
            num_total_removed_edges += num_remove_edges
            if num_remove_edges <= self.min_removed_edge:
                print('stop. current edges: {}'.format(num_total_removed_edges))
                break
            print('reomve {} edges. current edges: {}'.format(num_remove_edges, num_total_removed_edges))
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
    
    def get_num_path(self, uncovered_path):
        count = 0
        for v in uncovered_path:
            count += len(uncovered_path[v])
        return count

    def store_labels(self, cover: TwoHopCover):
        v = cover.center
        labels = self.labels
        labels[v]['in'][v] = 0
        labels[v]['out'][v] = 0
        # print('v: {}'.format(v))
        in_label = {in_v for in_v in labels[v]['in']}
        # print('in label: {}'.format(in_label))
        for in_v in cover.ancs:
            out_label = {out_v for out_v in labels[in_v]['out']}
            # print('in v: {}'.format(in_v))
            # print('out label: {}'.format(out_label))
            if not (in_label & out_label):
                labels[in_v]['out'][v] = cover.ancs[in_v]
            else:
                for mid_v in (in_label & out_label):
                    if labels[in_v]['out'][mid_v] + labels[v]['in'][mid_v] > cover.ancs[in_v]:
                        labels[in_v]['out'][v] = cover.ancs[in_v]

        out_label = {out_v for out_v in labels[v]['out']}
        for out_v in cover.desc:
            in_label = {in_v for in_v in labels[out_v]['in']}
            if not (in_label & out_label):
                labels[out_v]['in'][v] = cover.desc[out_v]
            else:
                for mid_v in (in_label & out_label):
                    if labels[v]['out'][mid_v] + labels[out_v]['in'][mid_v] > cover.desc[out_v]:
                        labels[out_v]['in'][v] = cover.desc[out_v]
    
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
    
def get_num_edges(G):
    count = 0
    for in_edges in G.adj_list_in:
        count += len(in_edges)
    return count