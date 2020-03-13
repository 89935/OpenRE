from graphviz import Digraph
import datetime
from graphviz import render
import json
def outputAsGraphForSet(resultSet):
    print("123")
    fontname = "FangSong"
    g = Digraph("Visualization")
    for result in resultSet:
        print(result)
        g.node(name=result[0], fontname="FangSong")
        g.node(name=result[2], fontname="FangSong")
        g.edge(result[0], result[2], fontname="FangSong", label=result[1])
        print(result)
    """
    neato 较差
    circo
    twopi
    fdp 
    """
    g.engine = 'circo'
    g.render('test-output/Visualization5.gv',view=True)

def readJsonToTriple(fileName):
    f = open('document-level-output\\' + fileName, 'r', encoding='utf-8')
    file = f.read()
    f.close()
    content = json.loads(file)  # 转化为json格式
    print(content)
    tripleList = []
    for key in content:
        entityPair = content[key]
        print(entityPair)
        for triple in entityPair:
            print(triple)
            for rel in triple[2]:
                tripleExample = []
                print(rel[0])
                rel_v = rel[0]
                relation = rel_v.split('_v')[0]
                print(relation)
                tripleExample.append(triple[0])
                tripleExample.append(relation)
                tripleExample.append(triple[1])
                print(tripleExample)
                tripleList.append(tripleExample)
    return tripleList

if __name__ == '__main__':
    # tripleList = readJsonToTriple("windowWord1_longestEntity_(loc-loc)+(loc-per)+(per-loc)+(per-per)+\\filtered-loc_loc_triples8.json")
    fileList = ['loc_loc_triples9.json','loc_per_triples9.json','loc_org_triples9.json',
                'per_loc_triples9.json','per_per_triples9.json','per_org_triples9.json',
                'org_loc_triples9.json','org_per_triples9.json','org_org_triples9.json']
    # fileList = ['windowWord1_longestEntity_60_30_(loc-loc)+(loc-per)+(per-loc)+(per-per)+\\filtered-loc_loc_triples8.json',
    #             'windowWord1_longestEntity_60_30_(loc-loc)+(loc-per)+(per-loc)+(per-per)+\\filtered-loc_per_triples8.json',
    #             'windowWord1_longestEntity_60_30_(loc-loc)+(loc-per)+(per-loc)+(per-per)+\\filtered-per_loc_triples8.json',
    #             'windowWord1_longestEntity_60_30_(loc-loc)+(loc-per)+(per-loc)+(per-per)+\\filtered-per_per_triples8.json',
    #             ]
    for fileName in fileList:
        tripleList = readJsonToTriple(fileName)
        file = r'C:\Users\thinkpad\Desktop\文档级进展\\' +fileName
        with open(file, 'a+',encoding='utf-8') as f:
            for triple in tripleList:
                f.write(triple[0]+','+triple[1]+','+triple[2] + '\n')  # 加\n换行显示
        print(tripleList)
        for triple in tripleList:
            print(triple[0]+','+triple[1]+','+triple[2])
    # tripleList = [['1','2','3']]
    # outputAsGraphForSet(tripleList)