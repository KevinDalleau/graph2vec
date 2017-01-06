import numpy as np

def bfs_level(graph, source, attributes):
    "Given a source node and an attributes list, returns a dictionary in the form {attribute1: level1, attribute2: level2,...,attributek: levelk}, where level corresponds to the level where this attribute has been reached from the source node"
    queues = [[source]]
    current_queue = None
    visited = set([])
    output = {attribute:np.Inf for attribute in attributes}
    level = 0
    while(queues):
        if(current_queue is None or current_queue == []):
            current_queue = queues.pop()
        if(len(current_queue) != 0):
            s = current_queue.pop(0)
        else:
            break
        if(len(queues)==0):
            queues.append([])
            level += 1
        for neighbour in graph[s]:
            if (neighbour not in visited):
                if(neighbour in attributes):
                    queues[0].append(neighbour)
                    output[neighbour] = level
                visited.add(neighbour)
    return output


def generate_graphs(graph_name):
    if(graph_name == "one"):
        adj_list = {}
        adj_list[1] = [2,3,6]
        adj_list[2] = [1,4]
        adj_list[3] = [1,5]
        adj_list[4] = [2,5]
        adj_list[5] = [3,4]
        adj_list[6] = [1,7]
        adj_list[7] = [6]
        individuals = [1,5,7]
    return((adj_list,individuals))

graph = generate_graphs("one")
graph_adj = graph[0]
graph_individuals = graph[1]
graph_attributes = set(graph_adj.keys())-set(graph_individuals)
output = bfs_level(graph_adj,7,graph_attributes);
print(output)

