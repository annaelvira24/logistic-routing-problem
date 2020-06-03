import networkx as nx
import matplotlib.pyplot as plt


# Visualize graph with specific order of tour
def visualize(graph, startCity, dest, nodes, tour):
    colors = ['r', 'b', 'g', 'black', 'magenta', 'orange', 'cyan', 'violet']
    myedges = []
    myedges.append((startCity, dest[0]))
    for i in range(len(dest)-1) :
        city = dest[i]
        graph.add_node(city, pos = (nodes.get(city).x, nodes.get(city).y))
        myedges.append((dest[i], dest[i+1]))
    
    graph.add_edges_from(myedges)
   
    position =nx.get_node_attributes(graph,'pos')
    nx.draw_networkx_nodes(graph, pos=position, cmap=plt.get_cmap('jet'), node_size = 500)
    nx.draw_networkx_labels(graph, pos=position)
    nx.draw_networkx_edges(graph, pos=position, edgelist = myedges, edge_color=colors[(tour)%8], arrows=True)

