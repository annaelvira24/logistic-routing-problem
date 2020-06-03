'''
Solving TSP with Branch and Bound Algorithm
References : https://www.geeksforgeeks.org/traveling-salesman-problem-using-branch-and-bound-2/ with some modifications
'''

import math 
maxsize = float('inf') 
  
# Copy temporary solution to the final solution 
def copyToFinal(currentPath, n): 
    finalPath[:n + 1] = currentPath[:] 
    finalPath[n] = currentPath[0] 
  
# Find the minimum edge cost having an end at the vertex i 
def firstMin(graph, i, n): 
    min = maxsize 
    for k in range(n): 
        if graph[i][k] < min and i != k: 
            min = graph[i][k] 
  
    return min
  
# find the second minimum edge cost having an end at the vertex i 
def secondMin(graph, i, n): 
    first, second = maxsize, maxsize 
    for j in range(n): 
        if i == j: 
            continue
        if graph[i][j] <= first: 
            second = first 
            first = graph[i][j] 
  
        elif(graph[i][j] <= second and 
             graph[i][j] != first): 
            second = graph[i][j] 
  
    return second 
  
# Recursive function of TSP
def TSPRec(graph, currentBound, currentWeight, level, currentPath, visited, n): 
    global finalResult
      
    # base case : when we have reached level n
    if level == n: 
          
        # check if there is an edge from last vertex in path back to the first vertex 
        if graph[currentPath[level - 1]][currentPath[0]] != 0: 
              
            # current Result has the total weight of the solution
            currentResult = currentWeight + graph[currentPath[level - 1]][currentPath[0]] 
            if currentResult < finalResult: 
                copyToFinal(currentPath, n) 
                finalResult = currentResult
        return
  
    # for other levels, we iterate them to built recursive tree
    for i in range(n): 
          
        # The next level vertex MUST diagonal entry in graphacency matrix and  
        # not visited already
        if (graph[currentPath[level-1]][i] != 0 and visited[i] == False): 
            temp = currentBound 
            currentWeight += graph[currentPath[level - 1]][i] 
  
            # compute the currentBound
            if level == 1: 
                currentBound -= ((firstMin(graph, currentPath[level - 1], n) + firstMin(graph, i, n)) / 2) 
            else: 
                currentBound -= ((secondMin(graph, currentPath[level - 1], n) + firstMin(graph, i, n)) / 2) 
  

            # If current lower bound < finalResult, explore the node further 
            if currentBound + currentWeight < finalResult: 
                currentPath[level] = i 
                visited[i] = True
                  
                # call TSPRec for the next level 
                TSPRec(graph, currentBound, currentWeight, level + 1, currentPath, visited, n) 
  
            # else, reset all changes to currentWeight and currentBound 
            currentWeight -= graph[currentPath[level - 1]][i] 
            currentBound = temp 
  
            visited = [False] * len(visited) 
            for j in range(level): 
                if currentPath[j] != -1: 
                    visited[currentPath[j]] = True
  

def TSP(graph, n): 
      
    # Initial lower bound for the root node  
    # 1/2 * (sum of first min + second min) for all edges
    currentBound = 0
    currentPath = [-1] * (n + 1) 
    visited = [False] * n
    global finalPath
    global finalResult
    finalPath = [None] * (n + 1)
    finalResult = maxsize
  
    # Compute initial bound 
    for i in range(n): 
        currentBound += (firstMin(graph, i, n) + secondMin(graph, i, n)) 
  
    currentBound = math.ceil(currentBound / 2) 
  
    visited[0] = True
    currentPath[0] = n-1
  
    TSPRec(graph, currentBound, 0, 1, currentPath, visited, n)
    return(finalResult, finalPath)
  