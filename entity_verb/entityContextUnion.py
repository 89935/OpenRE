import json
import csv
import thulac

thulac1 = thulac.thulac()
f = open('entity_verb_result\\' + "context_only_word_freq_dict.json"
             , 'r', encoding='utf-8')
file = f.read()
json_file = json.loads(file)
all_entity = json_file.keys()
all_entity = ["外朝","中和殿"]
print(all_entity)
all_entity_intersection = []
row1 = [" "]
for i in all_entity:
    row1.append(i)
all_entity_intersection.append(row1)
for A in all_entity:
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

        entityB_related = dictB.keys()
        intersection=list(set(entityA_related).intersection(set(entityB_related)))
        intersection_dict = dict()
        for i in intersection:
            intersection_dict[i] = [dictA[i],dictB[i]]
        # print(dictA)
        # print(dictB)
        print(intersection)
        # print(intersection_dict)
        intersection_dict = sorted(intersection_dict.items(), key=lambda item: sum(item[1]), reverse=True)
        list_A.append(intersection_dict)
        # print(list_A)
    all_entity_intersection.append(list_A)

with open('entity_verb_result\\intersection_only_verb.csv', 'w', newline='',encoding="utf-8") as t_file:
    csv_writer = csv.writer(t_file)
    for l in all_entity_intersection:
        # print(l)
        csv_writer.writerow(l)