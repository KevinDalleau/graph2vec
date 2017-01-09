import numpy as np
from scipy.sparse import coo_matrix


def get_paths_source(graph, source, individuals):
    "From a source node and given a list of individual nodes, returns the depths of the paths between the source node and all other attribute nodes"
    queue = [(source, [source])]
    attributes = set(graph.keys()) - set(individuals)
    output = {attribute:np.Inf for attribute in attributes}

    while queue:
        vertex, path = queue.pop(0)
        for next in set(graph[vertex]) - set(path):
            if (next not in individuals):
                queue.append((next,path+[next]))
                depth = len(path)
                if (output[next] == np.Inf):
                    output[next] = depth
                elif (output[next] is not 1):
                    output[next] -= float(1)/depth
 
    return output

def bfs_level(graph, individuals):
    rows = []
    cols = []
    data = []
    for individual in individuals:
        bfs_local = get_paths_source(graph,individual,individuals)
        cols_local = bfs_local.keys()
        data_local = get_similarity(bfs_local.values())
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
        adj_list[3] = [1,4,5]
        adj_list[4] = [2,3,5]
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

