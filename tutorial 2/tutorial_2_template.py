import collections as c
import time
import numpy as np

class UndirectedGraph(object):
  def __init__(self, edge_list):
      self.vertex_dict = {}
      self.adj_list = []
      self.vertex_num = 0
      for [src, dst] in edge_list:
          self.add_edge(src, dst)

  def add_vertex(self, name):
      id = self.vertex_num
      self.vertex_dict[name] = id
      self.vertex_num += 1
      self.adj_list.append(set())

  def add_edge(self, vertex1, vertex2):
      if vertex1 != vertex2:
          if vertex1 not in self.vertex_dict.keys():
              self.add_vertex(vertex1)
          if vertex2 not in self.vertex_dict.keys():
              self.add_vertex(vertex2)
          self.adj_list[self.vertex_dict[vertex1]].add(vertex2)
          self.adj_list[self.vertex_dict[vertex2]].add(vertex1)
  
  def print_G(self):
    print(self.vertex_dict)
    print(self.adj_list)
    print(self.vertex_num)
  
class DirectedGraph(object):
  def __init__(self, edge_list):
      self.vertex_dict = {}
      self.adj_list_in = []
      self.adj_list_out = []
      self.vertex_num = 0
      for [src, dst] in edge_list:
          self.add_edge(src, dst)

  def add_vertex(self, name):
      id = self.vertex_num
      self.vertex_dict[name] = id
      self.vertex_num += 1
      self.adj_list_in.append(set())
      self.adj_list_out.append(set())

  def add_edge(self, vertex1, vertex2):
      if vertex1 not in self.vertex_dict.keys():
          self.add_vertex(vertex1)
      if vertex2 not in self.vertex_dict.keys():
          self.add_vertex(vertex2)
      self.adj_list_out[self.vertex_dict[vertex1]].add(vertex2)
      self.adj_list_in[self.vertex_dict[vertex2]].add(vertex1)


class QuickFind:
  def __init__(self, N):
      self.N = N
      self.count = N
      self.root = []
      for i in range(0, self.N):
          self.root.append(i)

  def union(self, p, q):
      # Implement the QuickFind algorithm here, define other functions for the class if needed
      if self.find(p) == self.find(q):
        return
      for i in range(0, self.N):
        if self.root[i] == self.root[q]:
          self.root[i] = self.root[p]
      self.count -= 1
      return
  
  def find(self, p):
    return self.root[p]

class UnionFind:
  def __init__(self, N):
      self.count = N
      self.root = []
      self.size = []
      for i in range(0, N):
          self.root.append(i)
          self.size.append(1)

  def union(self, p, q):
      # Implement the union-find algorithm here, define other functions for the class if needed
      i = self.find(p)
      j = self.find(q)
      if i == j:
        return
      if self.size[i] < self.size[j]:
        self.size[j] += self.size[i]
        self.root[i] = j
      else: 
        self.size[i] += self.size[j]
        self.root[j] = i
      self.count -= 1
      return

  def find(self, p):
    while self.root[p] != p:
      p = self.root[p]
    return p

def connectComponents(G, method='SmartUnion', PrintRoots=True):
  if method == 'QuickFind':
    print("using QuickFind")
    conn_comp_G = QuickFind(G.vertex_num)
  else:
    print("using SmartUnion")    
    conn_comp_G = UnionFind(G.vertex_num)
  for i in range(G.vertex_num):
      u = i
      for j in G.adj_list[u]:
          v = G.vertex_dict[j]
          conn_comp_G.union(u, v)
  if PrintRoots:
    for id, seq in G.vertex_dict.items():
        print(id + "'s root is " + str(conn_comp_G.root[seq]))
  print("total number of connected components: " + str(conn_comp_G.count))


def topoSorting(G):
  # Implement your topological sorting algorithm here
  visited = []
  q = c.deque()
  for v in G.vertex_dict:
    if len(G.adj_list_in[G.vertex_dict[v]]) == 0:
      q.append(v)
  
  while len(q) != 0:
    v_in = q.popleft()
    visited.append(v_in)
    for v in G.vertex_dict:
      if v_in in G.adj_list_in[G.vertex_dict[v]]:
        G.adj_list_in[G.vertex_dict[v]].remove(v_in)
    for v in G.vertex_dict:
      if len(G.adj_list_in[G.vertex_dict[v]]) == 0 and v not in visited and v not in q:
        q.append(v)
  # print(G.vertex_dict)
  # print(G.adj_list_in)
  # print(G.adj_list_out)
  print(visited)
  return


if __name__ == "__main__":

  # Exercise 1
  edge_list_fig1 = [['a', 'b'],
                    ['c', 'd'],
                    ['c', 'h'],
                    ['d', 'h'],
                    ['e', 'f'],
                    ['e', 'g'],
                    ['f', 'g'],
                    ['g', 'i']]
  G_fig1 = UndirectedGraph(edge_list_fig1)
  connectComponents(G_fig1, 'QuickFind', PrintRoots=True)
  connectComponents(G_fig1, 'SmartUnion', PrintRoots=True)
  
  
  # Exercise 2
  # edge_list_dataset = np.loadtxt('dataset_30k.txt', dtype='int',delimiter=',')
  # G_dataset = UndirectedGraph(edge_list_dataset)
  # start_QuickFind = time.time()
  # connectComponents(G_dataset, 'QuickFind', PrintRoots=False)
  # start_SmartUnion = time.time()
  # connectComponents(G_dataset, 'SmartUnion', PrintRoots=False)
  # end_SmartUnion = time.time()
  # print("TIME of running QuickFind in DATASET: " + str(start_SmartUnion-start_QuickFind))
  # print("TIME of running SmartUnion in DATASET: " + str(end_SmartUnion-start_SmartUnion))

  # Exercise 3
  edge_list_fig2 = [['b', 'a'],
                    ['b', 'd'],
                    ['a', 'c'],
                    ['d', 'c'],
                    ['a', 'e'],
                    ['c', 'h'],
                    ['e', 'c'],
                    ['e', 'g'],
                    ['h', 'g'],
                    ['g', 'f'],
                    ['g', 'i']]

  G_fig2 = DirectedGraph(edge_list_fig2)
  topoSorting(G_fig2)
