import numpy as np
import rdflib
import time

class graph2vec():
    def __init__(self):
        self.graph_matrix = None
        self.vectors = None
        self.individuals = None

    def fit(self, graph, individuals):
        self.graph_matrix = graph
        self.individuals = individuals
        return self

    def fit_rdf(self, rdf):
        
        return 1

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


class rdf2adj():
    def __init__(self):
        self.graph_adj = {}
        self.individuals = None
        self.individualsDict = {} # To retrieve individual names
        self.attributes = None
        self.attributesDict = {} # To retrieve attributes names
        self.rdf = None
        self.offset = len(self.individualsDict)


    def fit(self,rdf, attributes=[(None,None)], individual=[(None,None)]):
        "Fits the object from a rdflib graph, a representation of attributes and individuals"

        self.rdf = rdf

        # LOADING INDIVIDUALS IN THE GRAPH 

        queryString = "SELECT ?individuals ?individualId WHERE {?individuals <http://www.graph.com/nodeType/>  \"individual\" . ?individuals <http://graph.com/identifier> ?individualId.}"
        res = self.rdf.query(queryString)
        for row in res:
            name =  str(row[0]).replace("http://graph.com/individual/","")
            indId = int(row[1])
            self.individualsDict[name] = indId

        # LOADING ATTRIBUTES IN THE GRAPH

        queryString = "SELECT ?attributes WHERE {?attributes <http://www.graph.com/nodeType/>  \"attribute\".}"
        res = self.rdf.query(queryString)
        i=1
        for row in res:
            name = str(row[0]).replace("http://graph.com/","")
            self.attributesDict[name] = i+self.offset
            i+=1

        # CONSTRUCTING THE ADJACENCY LIST
        queryString = "SELECT DISTINCT ?individual ?attribute WHERE {?individual <http://www.graph.com/nodeType/> \"individual\". ?individual <http://graph.com/relation/linked> ?attribute. ?attribute <http://www.graph.com/nodeType/> \"attribute\"}"
        res= self.rdf.query(queryString)
        for row in res:
            individualName = str(row[0]).replace("http://graph.com/individual/","")
            attributeName = str(row[1]).replace("http://graph.com/","")
            individualIndex = self.individualsDict[individualName]
            attributeIndex = self.attributesDict[attributeName]
            if individualIndex not in self.graph_adj:
                self.graph_adj[individualIndex] = set()
            if attributeIndex not in self.graph_adj:
                self.graph_adj[attributeIndex] = set()
            self.graph_adj[individualIndex].add(attributeIndex)
            self.graph_adj[attributeIndex].add(individualIndex)

        queryString = "SELECT DISTINCT ?attribute1 ?commonAttribute WHERE { ?attribute1 <http://www.graph.com/nodeType/> \"attribute\". ?commonAttribute <http://www.graph.com/nodeType/> \"attribute\". ?attribute1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?commonAttribute.}"
        res= self.rdf.query(queryString)
        for row in res:
            attributeName = str(row[0]).replace("http://graph.com/","")
            commonAttributeName = str(row[1]).replace("http://graph.com/","")
            attributeIndex = self.attributesDict[attributeName]
            commonAttributeIndex = self.attributesDict[commonAttributeName]
            if attributeIndex not in self.graph_adj:
                self.graph_adj[attributeIndex] = set()
            if commonAttributeIndex not in self.graph_adj:
                self.graph_adj[commonAttributeIndex] = set()
            self.graph_adj[attributeIndex].add(commonAttributeIndex)
            self.graph_adj[commonAttributeIndex].add(attributeIndex)


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
