import numpy as np
from scipy.sparse import coo_matrix

def bfs_level_source(graph, source, attributes):
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
                    value = output[neighbour]
                    if(value == np.Inf):
                        output[neighbour] = level
                    else:
                        output[neighbour]+= 1/level
                visited.add(neighbour)
    return output

def bfs_level(graph, individuals):
    attributes = set(graph) - set(individuals)
    rows = []
    cols = []
    data = []
    for individual in individuals:
        bfs_local = bfs_level_source(graph,individual,attributes)
        cols_local = bfs_local.keys()
        data_local = bfs_local.values()
        rows_local = [individual for x in range(len(data_local))]
        rows.extend(rows_local)
        cols.extend(cols_local)
        data.extend(data_local)
    output = coo_matrix((data,(rows,cols)))
    return output

def dict_to_list(dict):
    return ([sub_dict[1] for sub_dict in dict.items()],dict.keys())

def get_similarity(vec):
    return [float(1)/x for x in vec]

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
output = bfs_level(graph_adj,graph_individuals);
print(output)

