import json

from LTPNLP.core.postProcess import setTheResult


def differenceBetweenAAndB(fileA, fileB,fileName):
    A_triples = json.loads(fileA)['result'+fileName]
    A_triples = setTheResult(A_triples)  # 去重
    B_triples = json.loads(fileB)['result'+fileName]
    B_triples = setTheResult(B_triples)  # 去重
    A_list = []
    for triple in A_triples:
        str = triple[0] + "--" + triple[1] + "--" + triple[2]
        A_list.append(str)
    B_list = []
    for triple in B_triples:
        str = triple[0] + "--" + triple[1] + "--" + triple[2]
        B_list.append(str)
    A_set = set(A_list)
    B_set = set(B_list)
    return A_set-B_set,B_set-A_set


if __name__ == "__main__":
    f_A = open("outputTripes\\带所有修饰-all-9.6-constraints4-inverse-SPOVerbDict-20203413340383195.json", 'r', encoding='utf-8')
    file_A = f_A.read()
    f_B = open("outputTripes\\带所有修饰-all-9.6-constraints4-inverse-SPOVerbDict-202034134559780856.json", 'r', encoding='utf-8')
    file_B = f_B.read()
    fileList = ['5A_恭王府.txt',"5A_北京故宫博物院.txt","5A_颐和园.txt","5A_天坛公园.txt","5A_慕田峪长城.txt"]
    for fileName in fileList:
        A_set_B_set,B_set_A_set = differenceBetweenAAndB(file_A,file_B,fileName)
        print(A_set_B_set)
        print(B_set_A_set)