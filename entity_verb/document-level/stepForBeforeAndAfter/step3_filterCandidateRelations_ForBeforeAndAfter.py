import step1_getIG_ForBeforeAndAfter,step2_getScore_ForBeforeAndAfter,step4_filterTriples_ForBeforeAndAfter
import json

def filterCandidateRel(type_list,N,K):
    """
    根据type_list，取IGCandidateRelationWords的前N个元素作为 IGList
    对于每一个type：
        scoreList(t) = scoreCandidateRelationWords(t)的前K个元素
        RelationWords(t) = scoreList(t) ∩ IGList
    type(IGList) = List
    type(scoreList) = Dict
    type(RelationWords) = Dict
    :param type_list: 实体对类型列表集合
    :param N: 给IG排序
    :param K: 给Score排序
    :return: RelationWords
    """
    IGCandidateRelationWords = step1_getIG_ForBeforeAndAfter.sortedByIG(type_list)  # 候选关系词按照IG(rel)值降序排列的结果
    if len(IGCandidateRelationWords)>=N:
        relAndIG = IGCandidateRelationWords[0:N] # 取IG值前N个
    else:
        relAndIG = IGCandidateRelationWords
    IGList = []
    for rel in relAndIG:
        IGList.append(rel[0])
    scoreCandidateRelationWords = step2_getScore_ForBeforeAndAfter.sortedByScore(type_list)  # 候选关系词按照score(rel,t)值降序排序结果
    scoreList = dict()  # 存储scoreCandidateRelationWords前K个结果
    relationWords = dict()  # 存储不同的type，scoreList(type)和IGList的交集
    relationWordsAndScore = dict()  # 存储不同的type，scoreList(type)和IGList的交集以及该词的Score
    for type in type_list:
        if len(scoreCandidateRelationWords[type])>=K:
            relList = scoreCandidateRelationWords[type][0:K]
        else:
            relList = scoreCandidateRelationWords[type]
        newList = []
        for rel in relList:
            newList.append(rel[0])
        scoreList[type] = newList
        onlyWordsList = list(set(IGList).intersection(set(scoreList[type])))  # RelationWords(t) = scoreList(t) ∩ IGList
        relationWords[type] = onlyWordsList
        wordAndScoreDict = dict()
        for word in onlyWordsList:
            for rel in relList:
                if rel[0] == word:
                    wordAndScoreDict[word] = rel[1]
        wordAndScoreDict = sorted(wordAndScoreDict.items(), key=lambda item: item[1], reverse=True)
        relationWordsAndScore[type] = wordAndScoreDict

    name = ""
    for type in type_list:
        name += "(" + type + ")+"
    step4_filterTriples_ForBeforeAndAfter.writeJsonFile(relationWords, type_list, name + "RelationWords.json")
    step4_filterTriples_ForBeforeAndAfter.writeJsonFile(relationWordsAndScore, type_list, name + "RelationWordsAndScore.json")
    return relationWords,relationWordsAndScore

def filterCandidateRelWithFile(type_list,N,K,IGCandidateRelationWords,scoreCandidateRelationWords):
    """
    已有IGList和scoreCandidateRelationWords文件
    :param type_list: 实体对类型集合
    :param N: 给IG排序
    :param K: 给Score排序
    :param IGCandidateRelationWords: 候选关系词按照IG(rel)值降序排列的结果
    :param scoreCandidateRelationWords: # 候选关系词按照score(rel,t)值降序排序结果
    :return:
    """
    relAndIG = IGCandidateRelationWords[0:N]  # 取IG值前K个
    IGList = []
    for rel in relAndIG:
        IGList.append(rel[0])
    scoreList = dict()  # 存储scoreCandidateRelationWords前K个结果
    relationWords = dict()  # 存储不同的type，scoreList(type)和IGList的交集
    relationWordsAndScore = dict()  # 存储不同的type，scoreList(type)和IGList的交集以及该词的Score
    for type in type_list:
        relList = scoreCandidateRelationWords[type][0:K]
        newList = []
        for rel in relList:
            newList.append(rel[0])
        scoreList[type] = newList
        onlyWordsList = list(set(IGList).intersection(set(scoreList[type])))  # RelationWords(t) = scoreList(t) ∩ IGList
        relationWords[type] = onlyWordsList
        wordAndScoreDict = dict()
        for word in onlyWordsList:
            for rel in relList:
                if rel[0] == word:
                    wordAndScoreDict[word] = rel[1]
        wordAndScoreDict = sorted(wordAndScoreDict.items(), key=lambda item: item[1], reverse=True)
        relationWordsAndScore[type] = wordAndScoreDict
    return relationWords,relationWordsAndScore

def readJsonFile(fileName):
    """
    读取Json文件
    :param fileName: 文件名
    :return:
    """
    f = open('..\\document-level-output\\' + fileName, 'r', encoding='utf-8')
    file = f.read()
    f.close()
    content = json.loads(file)  # 转化为json格式
    return content

if __name__ == "__main__":
    type_list = ['loc-loc', 'loc-per']
    # relationWords = filterCandidateRel(type_list,300,200)
    scoreCandidateRelationWords_file_name = "(loc-loc)+(loc-per)+score.json"
    IGCandidateRelationWords_file_name = "(loc-loc)+(loc-per)+IG.json"
    scoreCandidateRelationWords = readJsonFile(scoreCandidateRelationWords_file_name)
    IGCandidateRelationWords = readJsonFile(IGCandidateRelationWords_file_name)
    relationWords,relationWordsAndScore = filterCandidateRel(type_list,100,50,IGCandidateRelationWords,scoreCandidateRelationWords)
    print(relationWords)
    print(relationWordsAndScore)
    name = ""
    for type in type_list:
        name += "(" + type + ")+"
    step4_filterTriples_ForBeforeAndAfter.writeJsonFile(relationWords, name + "RelationWords.json")
    step4_filterTriples_ForBeforeAndAfter.writeJsonFile(relationWordsAndScore, name + "RelationWordsAndScore.json")