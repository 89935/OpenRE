import step3_filterCandidateRelations
import json

file_path = "document-level-output\\"
file_name_dict = dict()
file_name_dict['loc-loc'] = "loc_loc_triples4.json"
file_name_dict['loc-per'] = "loc_per_triples4.json"
file_name_dict['loc-org'] = "loc_org_triples4.json"
file_name_dict['per-per'] = "per_per_triples4.json"
file_name_dict['per-org'] = "per_org_triples4.json"
file_name_dict['org-org'] = "org_org_triples4.json"
def filterTriplesByType(type,relationWords,candidateTriples):
    """
    指定实体对类型，根据relationWords(type)过滤掉该类型的候选三元组
    :param type:
    :param relationWords:
    :param candidateTriples:
    :return:
    """
    filteredTriplesDict = dict()
    for key in candidateTriples:
        values = candidateTriples[key]
        newList = []
        for value in values:
            newList1 = []
            relList = value[2]
            # relList = eval(relList)
            newList2 = []
            for rel in relList:
                # print(value[0] + "------"+value[1]+" : "+rel[0])
                if rel[0] in relationWords[type]:
                    # print("√")
                    newList2.append(tuple(rel))
            if len(newList2)!=0:
                newList1.append(value[0])
                newList1.append(value[1])
                newList1.append(newList2)
                newList.append(newList1)
        if len(newList)!=0:
            filteredTriplesDict[key] = newList
    return filteredTriplesDict


def filterAllTriples(type_list,relationWords):
    """
    给定实体对类型列表，获得属于类型列表的所有候选三元组，和relationWords（关系词组）。
    根据不同类型的relationWords来过滤各自类型的候选三元组
    :param type_list:
    :param relationWords:
    :return:
    """
    for type in type_list:
        candidateTriples_file_name =  file_name_dict[type]
        candidateTriples = step3_filterCandidateRelations.readJsonFile(candidateTriples_file_name)
        filteredTriplesDict = filterTriplesByType(type,relationWords,candidateTriples=candidateTriples)
        print(filteredTriplesDict)
        writeJsonFile(filteredTriplesDict,type_list,"filtered-"+file_name_dict[type])

def writeJsonFile(jsonDict,type_list,fileName):
    """
    写入Json文件
    :param jsonDict: 内容
    :param fileName: 文件名
    """
    filePath = ""
    for type in type_list:
        filePath += "(" + type + ")+"
    with open('document-level-output\\windowWord1'+filePath+"\\"+fileName, 'w',encoding='utf-8') as json_file:
        json_file.write(json.dumps(jsonDict, ensure_ascii=False))


if __name__ == "__main__":
    # type_list = ['loc-loc', 'loc-per']
    # # relationWords = filterCandidateRel(type_list,300,200)
    # scoreCandidateRelationWords_file_name = "(loc-loc)+(loc-per)+score.json"
    # IGCandidateRelationWords_file_name = "(loc-loc)+(loc-per)+IG.json"
    # candidateTriples_file_name = "loc_loc_triples.json"
    # scoreCandidateRelationWords = filterCandidateRelations.readJsonFile(scoreCandidateRelationWords_file_name)
    # IGCandidateRelationWords = filterCandidateRelations.readJsonFile(IGCandidateRelationWords_file_name)
    # relationWords, relationWordsAndScore = filterCandidateRelations.filterCandidateRel(type_list, 100, 50, IGCandidateRelationWords,
    #                                                                                  scoreCandidateRelationWords)
    #
    type_list = ['loc-loc', 'loc-per','per-per']
    relationWords,relationWordsAndScore = step3_filterCandidateRelations.filterCandidateRel(type_list, 100, 50)
    print(relationWords)
    filterAllTriples(type_list,relationWords)
