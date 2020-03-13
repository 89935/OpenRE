import json
import csv
import os

from step0_classifiedEntity import thulacFilter

f = open('..\\entity_verb_result\\' + "context_word_freq_dict_v5_one_sentence_beforeAndAfter.json"
             , 'r', encoding='utf-8')
file = f.read()
json_file = json.loads(file)
all_entity = json_file.keys()
# all_entity = ["外朝","中和殿"]
print(all_entity)
verbFrequencedict = dict()
for A in all_entity:
    list_A = []
    list_A.append(A)
    entityA = json_file[A]
    # print(entityA)
    entityA_related_only_verb = []
    for i in entityA:
        rel_word = i[0].split('_')[0]
        # print(rel_word)
        if thulacFilter(rel_word) == True:
            entityA_related_only_verb.append(i)
        else:
            print("thu"+rel_word)
        # if "v" in i[0]:
        #     rel_word = i[0].split('_v')[0]
        #     if thulacFilter(rel_word) == True:
        #         entityA_related_only_verb.append(i)
        #     else:
        #         print("thu"+i[0])

    # print(entityA_related_only_verb)
    verbFrequencedict[A] = entityA_related_only_verb
print(verbFrequencedict)

with open('document-level-output\\context_word_freq_dict_only_verb_thuFilter_one_sentence.json', 'w',
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(verbFrequencedict, ensure_ascii=False))

