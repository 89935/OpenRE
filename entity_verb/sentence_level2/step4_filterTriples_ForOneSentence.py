import step3_filterCandidateRelations_ForOneSentence
import json
file_path = "sentence_level2_result\\V0.1\\"
file_name_dict = dict()
file_name_dict['loc-loc'] = "loc_loc_triples.json"
file_name_dict['loc-per'] = "loc_per_triples.json"
file_name_dict['per-loc'] = "per_loc_triples.json"
file_name_dict['loc-org'] = "loc_org_triples.json"
file_name_dict['per-per'] = "per_per_triples.json"
file_name_dict['per-org'] = "per_org_triples.json"
file_name_dict['org-org'] = "org_org_triples.json"
def filterTriplesByType(type,relationWords,candidateTriples):
    """
    指定实体对类型，根据relationWords(type)过滤掉该类型的候选三元组
    :param type:
    :param relationWords:
    :param candidateTriples:
    :return:
    """
    filteredTriples = []

    for triple in candidateTriples:
        relation = triple[1]
        if relation in relationWords[type]:
            filteredTriples.append(triple)

    return filteredTriples


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
        candidateTriples = step3_filterCandidateRelations_ForOneSentence.readJsonFile(candidateTriples_file_name)
        filteredTriplesList = filterTriplesByType(type,relationWords,candidateTriples=candidateTriples)
        print(filteredTriplesList)
        with open(file_path + "filtered-"+file_name_dict[type], 'w',
                  encoding='utf-8') as json_file:
            json_file.write(json.dumps(filteredTriplesList, ensure_ascii=False))

if __name__ == "__main__":
    # type_list = ['loc-loc', 'loc-per']
    # relationWords = step3_filterCandidateRelations_ForOneSentence.readJsonFile('RelationWords.json')
    # filterAllTriples(type_list, relationWords)

    # # relationWords = filterCandidateRel(type_list,300,200)
    # scoreCandidateRelationWords_file_name = "(loc-loc)+(loc-per)+score.json"
    # IGCandidateRelationWords_file_name = "(loc-loc)+(loc-per)+IG.json"
    # candidateTriples_file_name = "loc_loc_triples.json"
    # scoreCandidateRelationWords = filterCandidateRelations.readJsonFile(scoreCandidateRelationWords_file_name)
    # IGCandidateRelationWords = filterCandidateRelations.readJsonFile(IGCandidateRelationWords_file_name)
    # relationWords, relationWordsAndScore = filterCandidateRelations.filterCandidateRel(type_list, 100, 50, IGCandidateRelationWords,
    #                                                                                  scoreCandidateRelationWords)
    #


    type_list = ['loc-loc', 'loc-per','per-loc','per-per']
    relationWords,relationWordsAndScore = step3_filterCandidateRelations_ForOneSentence.filterCandidateRel(type_list, 20, 10)
    print(relationWords)
    filterAllTriples(type_list,relationWords)
