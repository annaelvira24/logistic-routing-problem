'''
Dijkstra algorithm to find a vertex distance to all other vertrices in a graph
Reference from https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/ with some modifications
'''

import sys

def dijkstra(graph, source, nodesInput):
    nNodes = len(graph[0])
    dist = [sys.maxsize] * nNodes
    dist[source] = 0
    sptSet = [False] * nNodes
    count = 0
   
    for i in range(nNodes): 
   
        # Pick the minimum distance vertex from the set of vertices not yet processed
        u = minDistance(graph, dist, sptSet)
   
        # Put the minimum distance vertex in the shotest path tree 
        if(u != -1):
            sptSet[u] = True
            if(u in nodesInput):
                count += 1
   
        # Update distance value of the adjacent vertices of the picked vertex 
        # if the current distance is greater than new distance and 
        # the vertex in not in the spt
            for v in range(nNodes): 
                if graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + graph[u][v]: 
                    dist[v] = round(dist[u] + graph[u][v], 2)
        
        if(count == len(nodesInput)):
            break

    return dist

    # function to find the vertex with minimum distance value which haven't included in spt yet
def minDistance(graph, dist, sptSet): 
    nNodes = len(graph[0])
    min = sys.maxsize
    min_index = -1
    # Search not nearest vertex not in the shortest path tree 
    for v in range(nNodes): 
        if dist[v] < min and sptSet[v] == False: 
            min = dist[v] 
            min_index = v 
   
    return min_index 