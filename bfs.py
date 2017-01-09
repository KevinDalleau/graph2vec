import numpy as np

class graph2vec():
    def __init__(self):
        self.graph_matrix = None
        self.vectors = None
        self.individuals = None

    def fit(self, graph, individuals):
        self.graph_matrix = graph
        self.individuals = individuals

    def get_paths_source(self,source):
        "From a source node and given a list of individual nodes, returns the depths of the paths between the source node and all other attribute nodes"
        individuals = self.individuals
        graph = self.graph_matrix
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

    def get_vectors(self):
        "Returns vectors representing each individual node in a tuple in the form (vector, basis)"
        individuals = self.individuals
        output = {individual:[] for individual in individuals}
        for individual in individuals:
            bfs_local = self.get_paths_source(individual)
            cols_local = bfs_local.keys()
            data_local = get_similarity(bfs_local.values())
            output[individual] = (data_local,cols_local)
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
g2v = graph2vec()
g2v.fit(graph_adj,graph_individuals)
output = g2v.get_vectors()
print(output)

