# -*- coding: utf-8 -*-
import json

from entity_verb.entity_verb_new import entity_verb_new
from LTPNLP.core.GraphvizOutput import outputAsGraphForList, outputAsGraphForSet
from LTPNLP.core.mapEntity import removeTheSame2, mapEntityForSet


def setTheResult(result_list):
    result = set([tuple(t) for t in result_list])
    return result







if __name__ == "__main__":
    entity_verb_new = entity_verb_new()
    all_entity = entity_verb_new.readAllEntity("../../entity_verb//entity_verb_result\\all_entity.json")
    f = open("outputTripes\\all-不加任何修饰-故宫-为-9.62020342312131074.json", 'r', encoding='utf-8')
    file = f.read()

    fileList = ['5A_恭王府.txt',"5A_北京故宫博物院.txt","5A_颐和园.txt","5A_天坛公园.txt","5A_慕田峪长城.txt"]
    for fileName in fileList:
        all_triples = json.loads(file)['result'+fileName]
        all_triples = setTheResult(all_triples) # 去重
        print(all_triples)
        all_triples = removeTheSame2(all_triples) # 合并
        print(all_triples)
        sbjAndRelSame = []

        outputDict = dict()
        outputDict['result'] = all_triples

        with open('outputTripes/2020.03.04'+fileName+'-去重.json', 'w',
                  encoding='utf-8') as json_file:
            json_file.write(json.dumps(outputDict, ensure_ascii=False))
        print(len(all_triples))
        outputAsGraphForSet(all_triples)