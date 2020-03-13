import step3_filterCandidateRelations
import json
from collections import Counter
from matplotlib import pyplot as plt

# file_path = "document-level-output\\"
# file_name_dict = dict()
# file_name_dict['loc-loc'] = "loc_loc_triples2.json"
# file_name_dict['loc-per'] = "loc_per_triples2.json"
# file_name_dict['loc-org'] = "loc_org_triples2.json"
# file_name_dict['per-per'] = "per_per_triples2.json"
# file_name_dict['per-org'] = "per_org_triples2.json"
# file_name_dict['org-org'] = "org_org_triples2.json"
#
frequenceList = []
f = open("..\\entity_verb_result\\name_place_organization_classification_v5.json","r",encoding="utf-8")
file = f.read()
person_entity = json.loads(file)['人--412']
location_entity = json.loads(file)['地点--500']
organization_entity = json.loads(file)['组织机构--71']
f.close()
numRel = []
contentDict = step3_filterCandidateRelations.readJsonFile("context_word_freq_dict_only_verb_thuFilter_one_sentence.json")
# print(contentDict)
for key in contentDict:
    if (key in person_entity) or (key in location_entity) or (key in organization_entity):
        print(key)
        value = contentDict[key]
        print(value)
        # print(len(value))
        # numRel.append(len(value))
        for relList in value:
            print(relList)
            frequenceList.append(relList[1])
            print(relList[1])
# print(frequenceList)
#             sumFrequenceList.append(relList[1][0]+relList[1][1])
#             print(relList[1][0])
#             print(relList[1][1])
#

# print(numRel)
# numCounted = Counter(numRel)
# print(numCounted)

# print(frequenceList)
# sumCounted = Counter(frequenceList)
# print(sumCounted)
# print(sumFrequenceList)
# sumCounted = Counter(sumFrequenceList)
# print(sumCounted)
# sum = 0
#
# for key in sumCounted:
#     sum += sumCounted[key]
# print(sum)
# sumFrequenceDict = dict()
# for key in sumCounted:
#     sumFrequenceDict[key] = round(sumCounted[key]/sum,4)
# print(sumFrequenceDict)
# sumFrequenceDict = sorted(sumFrequenceDict.items(), key=lambda item: item[0])
# print(sumFrequenceDict)
# sum = 0
# sumDict = dict()
# for key in sumFrequenceDict:
#     sum += key[1]
#     sumDict[key[0]] = sum
# print(sumDict)
# sumFrequenceProb = []
# for key in sumDict:
#     sumFrequenceProb.append(sumDict[key])
# print(sumFrequenceProb)


counted = Counter(frequenceList)
print(counted)
sum = 0

for key in counted:
    sum += counted[key]
print(sum)
frequenceDict = dict()
for key in counted:
    frequenceDict[key] = round(counted[key]/sum,4)
frequenceDict = sorted(frequenceDict.items(), key=lambda item: item[0])
print(frequenceDict)
sum = 0
sumDict = dict()
for key in frequenceDict:
    sum += key[1]
    sumDict[key[0]] = sum
print(sumDict)
# # sumDict = sorted(sumDict.items(), key=lambda item: item[0])
# # print(sumDict)
#
frequenceProb = []
for key in sumDict:
    frequenceProb.append(sumDict[key])
print(frequenceProb)
# # plt.hist(frequenceList,[1,2,3,4,5,6,7,8,9,10,11,12],density=True)
# # # plt.xlabel(Xlabel)
# # plt.xlim(0,13)
# # # plt.ylabel(Ylabel)
# # # plt.ylim(Ymin,Ymax)
# # # plt.title(Title)
# # plt.show()