
from point import *

# Loads node file and store them in a dictionary
def loadNodes(file):
    nodes = {}
    
    f = open(file)
    content = f.read()
    lines = content.split('\n')
    f.close()

    for line in lines :
        temp = line.split(' ')
        if(len(temp) == 3):
            nodes[int(temp[0])] = Point(float(temp[1]), float(temp[2]))

    return nodes


# loads edges file and store them in an array
def loadEdges(file):
    edges = []

    f = open(file)
    content = f.read()
    lines = content.split('\n')
    f.close()

    for line in lines:
        temp = line.split(' ')
        if(len(temp) == 4):
            edges.append([int(temp[1]),int(temp[2]), round(float(temp[3]), 2)])
            edges.append([int(temp[2]),int(temp[1]), round(float(temp[3]), 2)])

    return edges
