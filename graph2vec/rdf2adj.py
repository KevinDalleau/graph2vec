import numpy as np
import rdflib

class Rdf2adj():
    def __init__(self):
        self.graph_adj = {}
        self.individuals = set()
        self.individualsDict = {} # To retrieve individual names
        self.attributes = set()
        self.attributesDict = {} # To retrieve attributes names
        self.rdf = None
        self.offset = 0
        self.y = {}

    def fit(self,rdf, individualsSpecifier="?r"):
        "Fits the object from a rdflib graph, given a relation to specify individuals in the form of (relation, object)"

        self.rdf = rdf

        # LOADING INDIVIDUALS IN THE GRAPH 

        indIterator = 1;
        
        queryString = "SELECT DISTINCT ?individuals ?class WHERE {?individuals %s ?class.}" % (individualsSpecifier) # I know I should use format, but wanted to avoid the hassle of doubling brackets here...

        res = self.rdf.query(queryString)
        for row in res:
            name =  row[0].encode('utf-8')#.rsplit('/',1)[1]
            indId = indIterator
            indIterator+=1
            self.individualsDict[name] = indId
            self.individuals.add(indId)
            self.y[indId] = row[1].encode('utf8')
            self.offset += 1 
        print("Individuals loaded")
        print("Number of individuals "+str(len(self.individuals)))

        # LOADING ATTRIBUTES IN THE GRAPH

       
        queryString = "SELECT DISTINCT ?attribute WHERE {?node ?relation ?attribute. FILTER NOT EXISTS {?node %s ?class. ?attribute %s ?class. }}" % (individualsSpecifier, individualsSpecifier)

        res = self.rdf.query(queryString)
        i=1
        for row in res:
            name = row[0].encode('utf-8')
            self.attributesDict[name] = i+self.offset
            self.attributes.add(i+self.offset)
            i+=1
        print("Attributes loaded")

  
        # CONSTRUCTING THE ADJACENCY LIST

        queryString = "SELECT DISTINCT ?individual ?attribute ?class WHERE {?individual %s ?class . ?individual ?relation ?attribute. }" % (individualsSpecifier)

        res= self.rdf.query(queryString)
        for row in res:
            individualName = row[0].encode('utf-8')
            attributeName = row[1].encode('utf-8')
            className = row[2].encode('utf-8')

            if(individualName in self.individualsDict and attributeName in self.attributesDict and attributeName != className):
                individualIndex = self.individualsDict[individualName]
                attributeIndex = self.attributesDict[attributeName]
                if individualIndex not in self.graph_adj:
                    self.graph_adj[individualIndex] = set()
                if attributeIndex not in self.graph_adj:
                    self.graph_adj[attributeIndex] = set()
                self.graph_adj[individualIndex].add(attributeIndex)
                self.graph_adj[attributeIndex].add(individualIndex)

        print("Ajdacency list half loaded")

        queryString = "SELECT DISTINCT ?node ?attribute WHERE {?node ?relation ?attribute. FILTER NOT EXISTS {?node %s ?class . ?attribute %s ?class .}}"  % (individualsSpecifier, individualsSpecifier)
        res= self.rdf.query(queryString)
        for row in res:
            attributeName = row[0].encode('utf-8')
            commonAttributeName = row[1].encode('utf-8')
            if(attributeName in self.attributesDict and commonAttributeName in self.attributesDict):
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

# graph = generate_graphs("one")
# graph_adj = graph[0]
# graph_individuals = graph[1]
# g2v = graph2vec()
# g2v.fit(graph_adj,graph_individuals)
# output = g2v.get_vectors()
# print(output)

