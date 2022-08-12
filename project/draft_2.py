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

class ShortestDistance(object):
    def __init__(self, G):
        self.G = G
        self.labels_in, self.labels_out = self.preprocess(G)
        # print(G.vertex_dict)
        # print('in:', self.labels_in)
        # print('out:', self.labels_out)


    def preprocess(self, G: DirectedWeightedGraph):
        labels_in = []
        labels_out = []
        for v in range(G.vertex_num):
            labels_in.append([]) 
            labels_out.append([]) 

        degree_pairs = self.get_graph_degree(G)
        highest_degree = self.get_highest_degree(degree_pairs)
        while highest_degree >= 0:
            for d_pair in degree_pairs:
                if highest_degree == d_pair[1]:
                    curr_v = d_pair[0]
                    d_pair[1] = -1
                    break
            # print(curr_v)
            for in_edge in G.adj_list_in[G.vertex_dict[curr_v]]:
                in_v = in_edge[0]
                in_dist = in_edge[1]

                (labels_out[G.vertex_dict[in_v]]).append([curr_v, in_dist])
                for out_label in labels_out[G.vertex_dict[in_v]]:
                    mid_v = out_label[0]
                    for in_label in labels_in[G.vertex_dict[curr_v]]:
                        potential_mid_v = in_label[0]
                        if mid_v == potential_mid_v:
                            if out_label[1] + in_label[1] > in_dist:
                                labels_out[G.vertex_dict[in_v]].remove(out_label)
                                labels_in[G.vertex_dict[curr_v]].remove(in_label)
                            elif out_label[1] + in_label[1] < in_dist:
                                labels_out[G.vertex_dict[in_v]].remove([curr_v, in_dist])



            for out_edge in G.adj_list_out[G.vertex_dict[curr_v]]:
                out_v = out_edge[0]
                out_dist = out_edge[1]
                
                labels_in[G.vertex_dict[out_v]].append([curr_v, out_dist])
                for in_label in labels_in[G.vertex_dict[out_v]]:
                    mid_v = in_label[0]
                    for out_label in labels_out[G.vertex_dict[curr_v]]:
                        potential_mid_v = out_label[0]
                        if mid_v == potential_mid_v:
                            if in_label[1] + out_label[1] > out_dist:
                                labels_in[G.vertex_dict[out_v]].remove(in_label)
                                labels_out[G.vertex_dict[curr_v]].remove(out_label)
                            elif in_label[1] + out_label[1] < out_dist:
                                labels_in[G.vertex_dict[out_v]].remove([curr_v, out_dist])
            
            highest_degree = self.get_highest_degree(degree_pairs)

        return (labels_in, labels_out)

    def query(self, source_vertex, target_vertex):
        vertices = list(self.G.vertex_dict.keys())
        # print('-------------QUERY START-------------')
        return self.recQuery(source_vertex, target_vertex, 0, vertices)
    
    def recQuery(self, src, dest, dist, unvisited):
        # print('src: {} dest: {} num unvisited: {}'.format(src, dest, len(unvisited)))
        if len(unvisited) == 0:
            return inf

        G = self.G
        labels_in = self.labels_in
        labels_out = self.labels_out

        for out_edge in labels_out[G.vertex_dict[src]]:
            out_v = out_edge[0]
            out_dist = out_edge[1]
            if out_v == dest:
                dist += out_dist
                # print('found')
                return dist
                
        for in_edge in labels_in[G.vertex_dict[dest]]:
            in_v = in_edge[0]
            in_dist = in_edge[1]
            if in_v == src:
                dist += in_dist
                # print('found')
                return dist
        
        curr_dist = inf
        # print('out edges: {}'.format(labels_out[G.vertex_dict[src]]))
        for out_edge in labels_out[G.vertex_dict[src]]:
            out_v = out_edge[0]
            out_dist = out_edge[1]
            try:
                unvisited.remove(out_v)
                # print('from {} to {}'.format(src, out_v))
                curr_dist = min(self.recQuery(out_v, dest, dist, copy.copy(unvisited)) + out_dist, curr_dist)
                # print('curr dist: {}'.format(curr_dist))
            except:
                # print('error, error node: {}, curr dist = {}'.format(out_v, curr_dist))
                pass

        # print('---out v: {}, src: {}, curr dist: {}---'.format(out_v, src, curr_dist))
        # print('in edges: {}'.format(labels_in[G.vertex_dict[dest]]))
        for in_edge in labels_in[G.vertex_dict[dest]]:
            in_v = in_edge[0]
            in_dist = in_edge[1]
            try:
                unvisited.remove(in_v)
                # print('from {} to {}'.format(in_v, dest))
                curr_dist =  min(self.recQuery(src, in_v, dist, copy.copy(unvisited)) + in_dist, curr_dist)
            except:
                # print('error, error node: {}, curr dist = {}'.format(in_v, curr_dist))
                pass
        
        # print('reach to bottom')
        return curr_dist
        

    def get_graph_degree(self, G: DirectedWeightedGraph):
        degrees = []
        vertices = list(G.vertex_dict.keys())
        for v in vertices:
            d = len(G.adj_list_in[G.vertex_dict[v]]) + len(G.adj_list_out[G.vertex_dict[v]])
            d_pair = [v, d]
            degrees.append(d_pair)
        return degrees

    def get_highest_degree(self, degree_pairs: list):
        degrees = []
        for d_pair in degree_pairs:
            degrees.append(d_pair[1])
        return max(degrees)

