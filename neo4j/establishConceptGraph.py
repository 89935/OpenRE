import os
from py2neo import *

class EstablishConceptGraph(object):
    """
    Build graph
    Node and Relation
    """
    def __init__(self,data_file = 'train.txt',data_name = 'travel_2'):
        self.graph = Graph(host = '39.107.127.64',auth = ('neo4j','tianyunzhe'))
        self.dataf = data_file
        self.dataname = data_name
        self.conceptNodeDict = self.freading()

    def freading(self):
        nodeSet = set()
        triples = []
        with open(self.dataf,'r',encoding='utf8') as f:
            line = f.readline().strip()
            while line:
                t = line.split(",")
                nodeSet.add(t[0])
                nodeSet.add(t[2])
                triples.append(t)
                line = f.readline().strip()
        entity_node = list(nodeSet)
        entity_node.sort()

        conceptNodeDict = dict()
        for i in range(len(entity_node)):
            idStr = 'entity'+str(i+1)
            conceptNodeDict[entity_node[i]] = idStr

        for t in triples:
            n1 = Node(self.dataname,name = t[0],id = conceptNodeDict[t[0]])
            n2 = Node(self.dataname,name = t[2],id = conceptNodeDict[t[2]])
            tx = self.graph.begin()
            rel = Relationship(n1,t[1],n2)
            tx.merge(n1,self.dataname,"id")
            tx.merge(n2,self.dataname,"id")
            tx.merge(rel)
            tx.commit()
        return conceptNodeDict


if __name__ == "__main__":
    conceptGraph = EstablishConceptGraph()