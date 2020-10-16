from collections import deque
from helper import reduce_nested_list

class Graph:
    def __init__(self):
        self.graph = {}
    
    def add_node(self, node, adjacency_list = []):
        self.graph[node] = adjacency_list
    
    # Find shortest Path using Breadth First Search
    def find_shortest_path(self, start, end):
        distance = {start: [start]}
        q = deque()
        q.append(start)
        while len(q):
            at = q.popleft()
            if at in self.graph:
                for next_elem in self.graph[at]:
                    if next_elem not in distance:
                        distance[next_elem] = [distance[at], next_elem]
                        q.append(next_elem)
        return distance[end] if end in distance else []
    
    def compute_distance(self, start, end):
        shortest_path = self.find_shortest_path(start, end)
        reduced_list = list(reduce_nested_list(shortest_path))
        return len(reduced_list) - 1
