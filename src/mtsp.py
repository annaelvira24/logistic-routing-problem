import math
import copy
import random
from itertools import product
from loadFiles import *
from graph import *
from tsp_bnb import *
from visualize import *
from mip import Model, xsum, minimize, BINARY
import networkx as nx
import matplotlib.pyplot as plt

def mtsp(nodes, edges, method):
    G = nx.DiGraph()
    fullGraph = graphMatrix(nodes, edges)
    nCity = int(input("Enter number of destination cities "))
    destCities = []
    print("enter the destination cities' ID ")
    i = 0
    while (i < nCity):
        dest = int(input())
        if(dest in destCities):
            print("City's already inputted")
        else:
            destCities.append(dest)
            i += 1
    
    startCity = int(input("Enter logistic office location "))
    while(startCity in destCities):
        print("City's already inputted")
        startCity = int(input("Enter logistic office location "))


    G.add_node(startCity, pos = (nodes.get(startCity).x, nodes.get(startCity).y))
    destCities.sort()

    nCourier = int(input("Enter number of courier available "))

    # City clustering with improved K-Means Algorithm
    # SETP 1 : Set the capacity of each cluster
    Q = math.ceil((nCity)/nCourier)

    # STEP 2 : Calculate the distance of each point to the cluster centre
    centroid = {}
    i = 0
    selected = []
    while (len(centroid)!=nCourier):
        randCentroid = random.choice(destCities)
        if(not(randCentroid in selected)):
            selected.append(randCentroid)
            centroid[i+1] = copy.deepcopy(nodes.get(randCentroid))
            i+=1

    countSame = 0
    while (countSame != nCourier):
        # STEP 3: Assign each point to cluster based on its ucledian distance to the cluster's centroid
        cityToCentroid = []
        for dest in destCities:
            for cent in centroid :
                distance = eucledian(nodes.get(dest), centroid.get(cent))
                cityToCentroid.append([distance, cent, dest])
            
        cityToCentroid.sort(key = lambda x:x[0])

        cityMapInClusters = {}
        for i in range (nCourier):
            cityMapInClusters[i+1] = []

        assigned = {}
        for i in destCities:
            assigned[i] = False

        count = 0
        while (count != nCity):
            for item in (cityToCentroid):
                if(len(cityMapInClusters.get(item[1]))< Q and assigned.get(item[2]) == False):
                    cityMapInClusters.get(item[1]).append(int(item[2]))
                    assigned[item[2]] = True
                    count += 1

        # Step 4 : The coordinates of the centroid is updated
        countSame = 0
        for cent in centroid :
            sumX = 0
            sumY = 0
            for i in range(len(cityMapInClusters.get(cent))):
                sumX += round(nodes.get(cityMapInClusters.get(cent)[i]).x,3)
                sumY += round(nodes.get(cityMapInClusters.get(cent)[i]).y,3)

            xCent = round((1/len(cityMapInClusters.get(cent))) * sumX, 0)
            yCent = round((1/len(cityMapInClusters.get(cent))) * sumY, 0)
            
            if(xCent == round(centroid.get(cent).x,0) and yCent == round(centroid.get(cent).y,0)):
                countSame += 1

            centroid.get(cent).x = xCent
            centroid.get(cent).y = yCent

    
    destCities.append(startCity)
    subGraph = subGraphMatrix(fullGraph, destCities)
    print("The full subgraph: ")
    printMatrix(subGraph, destCities)
    print()
    # Searching solution for TSP of each cluster
    for tour in range (nCourier):
        n = len(cityMapInClusters.get(tour+1))
        dest = cityMapInClusters.get(tour+1)
        dest.sort()
        dest.append(startCity) 
        places = cityMapInClusters.get(tour+1)
        V = set(range(len(cityMapInClusters.get(tour+1))))
        c = subGraphMatrix(fullGraph, dest)

        print("=========================================================")
        print("Tour", str(tour+1), ":")
        print("Subgraph Matrix:")
        printMatrix(c, dest)
        print()

        # use the original BnB algorithm
        if(method == '1'):
            finalResult, finalPath = TSP(c, len(dest))
                   
            print('route with total distance found: ', finalResult)
            print(finalPath)
            print(startCity, end = "")
            subdest = []
            for i in range (1,len(finalPath)):
                print(" ->", places[finalPath[i]], end = "")
                subdest.append(places[finalPath[i]])
        
        # TSP optimization using mip
        else:
            model = Model()
            x = [[model.add_var(var_type=BINARY) for j in V] for i in V]
            y = [model.add_var() for i in V]

            # objective function: minimize the distance
            model.objective = minimize(xsum(c[i][j]*x[i][j] for i in V for j in V))

            # constraint : leave each point only once
            for i in V:
                model += xsum(x[i][j] for j in V - {i}) == 1

            # constraint : enter each point only once
            for i in V:
                model += xsum(x[j][i] for j in V - {i}) == 1

            # subtour elimination
            for (i, j) in product(V - {n}, V - {n}):
                if i != j:
                    model += y[i] - (n+1)*x[i][j] >= y[j]-n

            # optimizing
            status = model.optimize(max_seconds=30)
            print(status)

            print("=========================================================")
            print("Tour", str(tour+1), ":")
            print("Subgraph Matrix:")
            printMatrix(c, dest)
            print("")

            # checking if a solution was found
            if model.num_solutions:
                print('route with total distance found: ', model.objective_value)
                print(startCity, end = "")
                nc = n
                subdest = []
                while True:
                    nc = [i for i in V if x[nc][i].x >= 0.99][0]
                    print(" ->", places[nc], end = "")
                    subdest.append(places[nc])
                    if nc == n:
                        break       
            else:
                print(model.objective_bound) 

        print("")
        print("")

        # visualize the graph
        visualize(G, startCity, subdest, nodes, tour)

    plt.show()


def eucledian(point1, point2):
    return (math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2))