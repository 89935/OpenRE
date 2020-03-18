import sys
import json
import math
import step1_getIG_ForOneSentence

file_path = "sentence_level2_result\\V0.1\\"
def getScore(types,rel):
    """
    score(rel,t):使用实体对类型打分公式来评价一个词语是否能描述特定实体对类型的关系
    :param types: 特定的实体对类型
    :param rel: 关系
    :return:
    """
    scoreDict = dict()
    probOfTGivenRelDict = step1_getIG_ForOneSentence.givenRelGetProbOfType(types, rel)  # 计算P(t|rel)，关系为rel的条件下，实体对类型为t的概率
    relAndTypeDict = step1_getIG_ForOneSentence.getRelTripes(types, rel)  # 计算C(rel,t):rel和t共线的次数
    print("p(t|rel)")
    print(probOfTGivenRelDict)
    print("C(t,rel)")
    print(relAndTypeDict)
    """
    score(rel,t) = 0.0 是因为c(rel,t) = 1 导致 logc(rel,t) = 0.0
    score(rel,t) = 0 是因为c(rel,t) = 0 导致 
    """
    for type in types:
        score = -1  # 改动！当c(rel,t)==0即P(t|rel)==0的情况下，将score设置为-1
        if probOfTGivenRelDict[type] != 0:
            score = probOfTGivenRelDict[type]*math.log2(relAndTypeDict[type])
        scoreDict[type] = score
    return scoreDict

def sortedByScore(types):
    """
    根据types，获得候选关系集合，根据score(rel,t)，对每个关系类型的score(rel,t)进行排序
    :param types: 实体对关系类型集合
    :return:
    """
    allCandidateRelSet = step1_getIG_ForOneSentence.getAllCandidateRel(types)
    # allCandidateRelSet = ["位于_v","召见_v"]
    scoreByTypeDict = dict()
    for type in types:
        newDict = dict()
        scoreByTypeDict[type] = newDict
    for candidateRel in allCandidateRelSet:
        print("----------------------------")
        print(candidateRel)
        scoreByRelDict = getScore(types,candidateRel)

        print("score(rel,t)")
        print(scoreByRelDict)
        for type in types:
            if scoreByRelDict[type]>=0:  # 当c(rel,t) == 0:即目前的数据中，没有rel和t共现的，所以在t类型中，就不用考虑rel，即不需要将score(rel)算在t里
                newDict = scoreByTypeDict[type]
                newDict[candidateRel] = scoreByRelDict[type]
    # print(scoreByTypeDict)
    sortedScoreByTypeDict = dict()
    for type in types:
        scoreByType = scoreByTypeDict[type]
        sortedScoreByType = sorted(scoreByType.items(), key=lambda item: item[1], reverse=True)
        sortedScoreByTypeDict[type] = sortedScoreByType

    name = ""
    for type in types:
        name += "(" + type + ")+"
    with open(file_path + 'Score.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(sortedScoreByTypeDict, ensure_ascii=False))

    return sortedScoreByTypeDict
    # for type in types:






if __name__ == "__main__":
    type_list = ['loc-loc','loc-per']
    # print(getScore(type_list ,"位于_v"))
    scoreDict = sortedByScore(type_list)
    # print(scoreDict)
    # name = ""
    # for type in type_list:
    #     name += "("+type+")+"
    # with open('document-level-output\\'+name+'score.json', 'w',
    #           encoding='utf-8') as json_file:
    #     json_file.write(json.dumps(scoreDict, ensure_ascii=False))