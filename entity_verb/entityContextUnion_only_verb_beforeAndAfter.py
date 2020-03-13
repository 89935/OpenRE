import json
import csv
import os



f = open('entity_verb_result\\' + "context_word_freq_dict_v6_longestEntity__one_sentence_beforeAndAfter2.json"
             , 'r', encoding='utf-8')
file = f.read()
json_file = json.loads(file)
all_entity = json_file.keys()
# all_entity = ["外朝","中和殿"]
print(all_entity)
all_entity_intersection = []
row1 = [" "]
for i in all_entity:
    row1.append(i)
all_entity_intersection.append(row1)
remain = len(all_entity)
for A in all_entity:
    remain = remain-1
    print(remain)
    list_A = []
    list_A.append(A)
    entityA = json_file[A]
    dictA = dict()
    for i in entityA:
        dictA[i[0]] = i[1]
    for B in all_entity:
        entityB = json_file[B]
        dictB = dict()
        for i in entityB:
            dictB[i[0]] = i[1]
        f.close()
        entityA_related = dictA.keys()
        # print(entityA_related)
        # entityA_related_only_verb = []
        # print(pos[0])
        # print(len(pos))
        entityA_related_only_verb=[]
        for word in entityA_related:
            """
            after代表动词在该实体后，即，实体在动词前：     中和殿  位于
            """
            if "after" in word:
                entityA_related_only_verb.append(word[:-6])
        # print(entityA_related_only_verb)

        entityB_related = dictB.keys()
        entityB_related_only_verb = []
        for word in entityB_related:
            """
            before代表动词在实体前，即，实体在动词后：      位于   外朝  
            """
            if "before" in word:
                entityB_related_only_verb.append(word[:-7])
        # print(entityB_related_only_verb)
        intersection=list(set(entityA_related_only_verb).intersection(set(entityB_related_only_verb)))
        intersection_dict = dict()
        for i in intersection:
            intersection_dict[i] = [dictA[i+'_after'],dictB[i+'_before']]
        # print(dictA)
        # print(dictB)
        # print(intersection)
        # print(intersection_dict)
        intersection_dict = sorted(intersection_dict.items(), key=lambda item: sum(item[1]), reverse=True)
        list_A.append(intersection_dict)
        # print(list_A)
    all_entity_intersection.append(list_A)
with open('entity_verb_result\\intersection_only_verb_windowWord_1_v6_longestEntity_one_sentence_beforeAndAfter.csv', 'w', newline='',encoding="utf-8") as t_file:
    csv_writer = csv.writer(t_file)
    for l in all_entity_intersection:
        # print(l)
        csv_writer.writerow(l)
# with open('entity_verb_result\\intersection_only_verb4.csv', 'w', newline='',encoding="utf-8") as t_file:
#     csv_writer = csv.writer(t_file)
#     for l in all_entity_intersection:
#         # print(l)
#         csv_writer.writerow(l)