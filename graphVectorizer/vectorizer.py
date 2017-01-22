import numpy as np

class Vectorizer():
    def __init__(self):
        self.graph_matrix = None
        self.vectors = None
        self.individuals = None

    def fit(self, graph, individuals):
        self.graph_matrix = graph
        self.individuals = individuals
        return self

    def get_paths_source(self, source, maxDepth=None, alpha = float(1)/2):
        "From a source node and given a list of individual nodes, returns the depths of the paths between the source node and all other attribute nodes"
        individuals = self.individuals
        graph = self.graph_matrix
        queue = [(source, [source])]
        attributes = set(graph.keys()) - set(individuals)
        output = {attribute:0 for attribute in attributes}
        depth = 1
        visited = set()

        while queue:
            if(depth==maxDepth):
                break

            vertex, path = queue.pop(0)
            for next in set(graph[vertex]) - set(path):
                if (next not in individuals and next not in visited):
                    queue.append((next,path+[next]))
                    visited.add(next)
                    depth = len(path)
                    output[next] += alpha**depth
 
        return output

    def get_vectors(self):
        "Returns vectors representing each individual node in a tuple in the form (vector, basis)"
        individuals = self.individuals
        output = {individual:[] for individual in individuals}
        for individual in individuals:
            bfs_local = self.get_paths_source(individual)
            cols_local = bfs_local.keys()
            data_local = bfs_local.values()
            output[individual] = (data_local,cols_local)
        return output

    def dict_to_list(self,dict):
        return ([sub_dict[1] for sub_dict in dict.items()],dict.keys())