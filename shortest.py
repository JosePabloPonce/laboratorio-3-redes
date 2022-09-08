from queue import PriorityQueue
from math import inf
import networkx as nx


def dijkstra(graph, start, end):

    def camino(prev, start, end):
        node = end
        path = []
        while node != start:
            path.append(node)
            node = prev[node]
        path.append(node) 
        path.reverse()
        return path
        
    prev = {} 
    dist = {v: inf for v in list(nx.nodes(graph))} 
    visited = set() 

    pq = PriorityQueue()  
    
    dist[start] = 0  
    pq.put((dist[start], start))
    
    while 0 != pq.qsize():
        curr_cost, curr = pq.get()
        visited.add(curr)
        for neighbor in dict(graph.adjacency()).get(curr):
            path = dist[curr] + 1
            if path < dist[neighbor]:
                dist[neighbor] = path
                prev[neighbor] = curr
                if neighbor not in visited:
                    visited.add(neighbor)
                    pq.put((dist[neighbor],neighbor))
                else:
                    _ = pq.get((dist[neighbor],neighbor))
                    pq.put((dist[neighbor],neighbor))

    return camino(prev, start, end)
    