from dijkstra import *

# create subgrah matrix from fullmatrix for inputed nodes
def subGraphMatrix(fullMatrix, nodesInput):
    n = len(nodesInput)
    matrix = [[-1 for j in range(n)] for i in range(n)]
    
    for i in range (n):
        dist = dijkstra(fullMatrix, nodesInput[i], nodesInput)
        for j in range (len(dist)):
            for k in range (len(nodesInput)):
                if(j == nodesInput[k]):
                    matrix[i][k] = dist[j]

    return matrix

# Creates matrix from given nodes and egdes 
def graphMatrix(nodes, edges):
    matrix = [[0 for j in range(len(nodes))] for i in range(len(nodes))]
    for item in edges:
        matrix[item[0]][item[1]] = item[2]
    
    return matrix
    
# Prit matrix in ordinary format
def printNormalMatrix(matrix):
    n = len(matrix[0])
    for i in range(n): 
        for j in range(n): 
            print(str(matrix[i][j]), end = "")
            if(len(str(matrix[i][j]))<7):  
                print('\t', end = "")
            else:
                print(" ", end = "")
        print()


# print matrix with row and column nodes' ID
def printMatrix(matrix, dest):
    n = len(matrix[0])
    print('-\t|', end = "")
    for i in range(len(dest)):
        print(str(dest[i]) + '\t', end = "")
    print()
    
    for i in range(len(dest)+1):
        print('-------', end = "")
    
    print()

    for i in range(n): 
        for j in range(n):
            if(j == 0):
                print(str(dest[i]) + "\t|", end = "")
            print(str(matrix[i][j]), end = "")
            if(len(str(matrix[i][j]))<=6):
                print("\t", end = "") 
            else:
                print(" ", end = "")

        print()