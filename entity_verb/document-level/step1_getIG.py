import json
import math

import step4_filterTriples

file_path = "document-level-output\\"
file_name_dict = dict()
file_name_dict['loc-loc'] = "loc_loc_triples4.json"
file_name_dict['loc-per'] = "loc_per_triples4.json"
file_name_dict['loc-org'] = "loc_org_triples4.json"
file_name_dict['per-per'] = "per_per_triples4.json"
file_name_dict['per-org'] = "per_org_triples4.json"
file_name_dict['org-org'] = "org_org_triples4.json"
def getEntropy(type_list):
    totalNum = getTotalNum(type_list)
    typeNumDict = getNumOfType(type_list)
    entropy = 0.0
    for type in type_list:
        typeNum = typeNumDict[type]
        p_type = typeNum/totalNum
        entropy -= p_type*math.log2(p_type)
    return entropy

def getConditionalEntropy(type_list,rel):
    """
    计算条件信息熵
    :param type_list: 实体对类型
    :param rel: 关系
    :return:
    """
    jointProbDictRelDict = getJointProb(type_list,rel) # 获得联合概率P(rel,t)
    probOfTGivenRelDict = givenRelGetProbOfType(type_list,rel) # 给定关系rel的条件下，各个实体对种类的条件概率p(t|rel)
    jointProbDictNotRelDict = getJointProbNotRel(type_list,rel) # 获得联合概率P(非rel,t)
    probOfTGivenNotRelDict = givenNotRelGetProbOfType(type_list,rel) # 给定关系不为rel的条件下，各个实体对种类的条件概率P(t|非rel)
    conditionalEntropy = 0
    for type in type_list:
        if jointProbDictRelDict[type]!=0:
            conditionalEntropy += jointProbDictRelDict[type]*math.log2(probOfTGivenRelDict[type])
    for type in type_list:
        conditionalEntropy += jointProbDictNotRelDict[type]*math.log2(probOfTGivenNotRelDict[type])
    return -conditionalEntropy

def getInformationGain(type_list,rel):
    entropy = getEntropy(type_list)
    conditionalEntropy = getConditionalEntropy(type_list,rel)
    IG = entropy - conditionalEntropy
    return IG

def getJointProb(types,rel):
    """
    P(type,rel)获得联合概率
    :param types:
    :param rel:
    :return:
    """
    relAndTypeDict = getNumOfTypeAndRel(types, rel)  # 获得rel和type共同存在的候选三元组数量
    totalNum = getTotalNum(types)
    relAndTypeProbDict = dict()
    for type in types:
        relAndTypeProbDict[type] = relAndTypeDict[type]/totalNum
    return relAndTypeProbDict


def getTotalNum(type_list):
    """
    获得所有候选三元组的个数
    :param type_list:
    :return:
    """
    totalNum = 0
    typeNumDict = getNumOfType(type_list)
    for type in typeNumDict:
        totalNum += typeNumDict[type]
    return totalNum


def givenRelGetProbOfType(types, rel):
    """
    P(t|rel)给定关系，候选三元组的实体对类型属于type的概率
    :param type:实体对类型
    :param rel: 关系
    :return:
    """
    conditionalPDict = dict()
    relNumDict = getRelTripes(types,rel)
    # print(relNumDict)
    totalNum = 0
    for type in types:
        totalNum += relNumDict[type]
    for type in types:
        conditionalPDict[type] = relNumDict[type]/totalNum
    return conditionalPDict

def givenNotRelGetProbOfType(types, rel):
    """
    P(t|非rel)给定关系不是rel，候选三元组的实体对类型属于type的概率
    :param type:实体对类型
    :param rel: 关系
    :return:
    """
    conditionalPDict = dict()
    notRelNumDict = getNumOfTypeAndNotRel(types,rel)
    totalNum = 0
    for type in types:
        totalNum += notRelNumDict[type]
    for type in types:
        conditionalPDict[type] = notRelNumDict[type]/totalNum
    return conditionalPDict



def getRelTripes(types,rel):
    """
    获得关系为rel的所有候选三元组集合的个数
    :param types: 实体类型对集合
    :param rel: 关系
    :return:
    """
    relDict = dict()
    for type in types:
        f = open(file_path + file_name_dict[type], "r", encoding="utf-8")
        file = f.read()
        triples = json.loads(file)
        count = 0
        for entityName in triples:
            for triple in triples[entityName]:
                rel_list = triple[2]
                # rel_list = eval(rel_list)
                for relation in rel_list:
                    if relation[0] == rel:
                        count +=1
        relDict[type] = count
    return relDict

def getJointProbNotRel(types,rel):
    """
    获得关系为rel和实体对类型是type的联合概率P(非rel,type)
    :param types:
    :param rel:
    :return:
    """
    typeAndNotRelDict = getNumOfTypeAndNotRel(types,rel)
    totalNum = getTotalNum(types)
    jointProbDict = dict()
    for type in types:
        jointProbDict[type] = typeAndNotRelDict[type]/totalNum
    return jointProbDict





def getNumOfTypeAndNotRel(types,rel):
    """
    P(非rel,t)关系不是rel，且实体对类型为t的数量
    :param types:实体对列表
    :param rel: 关系
    :return:
    """
    relAndTypeDict = getNumOfTypeAndRel(types,rel)
    typeNumDict = getNumOfType(types)
    notRelAndTypeDict = dict()
    for type in types:
        notRelAndTypeDict[type] = typeNumDict[type] - relAndTypeDict[type]
    return notRelAndTypeDict

def getNumOfTypeAndRel(types,rel):
    """
    P(rel,t)关系为rel且实体对类型为type的数量
    :param types:实体对类型
    :param rel: 关系
    :return:
    """
    relAndTypeDict = dict()
    for type in types:
        f = open(file_path + file_name_dict[type], "r", encoding="utf-8")
        file = f.read()
        triples = json.loads(file)
        count = 0
        for entityName in triples:
             for triple in triples[entityName]:
                 # print(triple)
                 rel_list = triple[2]
                 # print(rel_list)
                 # rel_list = eval(rel_list)

                 for relation in rel_list:
                     if relation[0] == rel:
                         # print(rel_list)
                         count +=1
        relAndTypeDict[type] = count
    return relAndTypeDict




def getNumOfType(types):
    """
    获得不同实体对类型的候选三元组的数目
    :param types:
    :return:
    """
    typeNumDict = dict()
    for type in types:
        f = open(file_path+file_name_dict[type], "r", encoding="utf-8")
        file = f.read()
        triples = json.loads(file)
        count = 0
        for entityName in triples:
            # print(triples[entityName])
            for relation_list in triples[entityName]:
                # rel_list = eval(relation_list[2])
                rel_list = relation_list[2]
                # print(relation_list[2])
                # print(len(rel_list))
                count += len(rel_list)
        typeNumDict[type] = count
        # print(count)
    return typeNumDict

def getAllCandidateRel(types):
    """
    获得所有的候选关系词集合
    :param types: 关系种类
    :return:
    """
    allCandidateRelList = []
    for type in types:
        f = open(file_path + file_name_dict[type], "r", encoding="utf-8")
        file = f.read()
        triples = json.loads(file)
        for entityName in triples:
            # print(triples[entityName])
            for relation_list in triples[entityName]:
                # rel_list = eval(relation_list[2])
                rel_list = relation_list[2]
                for rel in rel_list:
                    allCandidateRelList.append(rel[0])
                    # print(rel)
        allCandidateRelSet = set(allCandidateRelList)
    return allCandidateRelSet

def sortedByIG(types):
    """
    根据types获得所有要计算的类型，以及所有的候选关系集合（针对于实体对类型），为每一个候选关系计算信息增益，再排序
    :param types: 实体对关系
    :return: 排序的IG
    """
    IGDict = dict()
    allCandidateRelSet = getAllCandidateRel(types)
    for candidateRel in allCandidateRelSet:
        IGDict[candidateRel] = getInformationGain(types,candidateRel)
    IGDict = sorted(IGDict.items(), key=lambda item: item[1], reverse=True)
    name = ""
    for type in types:
        name += "(" + type + ")+"
    step4_filterTriples.writeJsonFile(IGDict, types, name + "IG.json")
    return IGDict

if __name__ == "__main__":
    type_list = ['loc-loc','loc-per']

    IGDict = sortedByIG(type_list)
    print(IGDict)
    name = ""
    for type in type_list:
        name += "(" + type + ")+"
    with open('document-level-output\\' + name + 'IG.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(IGDict, ensure_ascii=False))


    # type_list = ['loc-loc','loc-per','loc-org','per-per','per-org']
    # print(getAllCandidateRel(types=type_list))
    # print(getNumOfType(type_list))
    # print(getEntropy(type_list))

    # print(getNumOfTypeAndRel(type_list,"位于_v"))
    # print("C(type|rel)")
    # print(getNumOfTypeAndRel(type_list,"位于_v"))
    # print("P(type|rel)")
    # print(givenRelGetProbOfType(type_list, "位于_v"))
    # print("联合概率P(type,rel)")
    # print(getJointProb(type_list, "位于_v"))
    # print("C(type|非rel)")
    # print(getNumOfTypeAndNotRel(type_list,"位于_v"))
    # print("联合概率P(type,非rel)")
    # print(getJointProbNotRel(type_list,"位于_v"))
    # print("P(type|非rel)")
    # print(givenNotRelGetProbOfType(type_list,"位于_v"))
    #
    # print(getTotalNum(type_list))
    # print(getConditionalEntropy(type_list,"位于_v"))
    # print("信息增益")
    # print(getInformationGain(type_list,"位于_v"))
    # print("信息增益")
    # print(getInformationGain(type_list,"建造_v"))
    # print("信息增益")
    # print(getInformationGain(type_list,"收藏_v"))
    # print("信息增益")
    # print(getInformationGain(type_list,"召见_v"))