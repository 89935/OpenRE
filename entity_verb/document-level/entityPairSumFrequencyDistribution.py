import step3_filterCandidateRelations
from collections import Counter
from matplotlib import pyplot as plt

file_path = "document-level-output\\"
file_name_dict = dict()
file_name_dict['loc-loc'] = "loc_loc_triples2.json"
file_name_dict['loc-per'] = "loc_per_triples2.json"
file_name_dict['loc-org'] = "loc_org_triples2.json"
file_name_dict['per-per'] = "per_per_triples2.json"
file_name_dict['per-org'] = "per_org_triples2.json"
file_name_dict['org-org'] = "org_org_triples2.json"

frequenceList = []
sumFrequenceList = []
type_list = ['loc-loc', 'loc-per','per-per']
for type in type_list:
    contentDict = step3_filterCandidateRelations.readJsonFile(file_name_dict[type])
    for key in contentDict:
        value = contentDict[key]
        print(value)
        for pair in value:
            print(pair)
            for relList in pair[2]:
                print(relList)
                frequenceList.append(relList[1][0])
                frequenceList.append(relList[1][1])
                sumFrequenceList.append(relList[1][0]+relList[1][1])
                print(relList[1][0])
                print(relList[1][1])

print(sumFrequenceList)
sumCounted = Counter(sumFrequenceList)
print(sumCounted)
sum = 0

for key in sumCounted:
    sum += sumCounted[key]
print(sum)
sumFrequenceDict = dict()
for key in sumCounted:
    sumFrequenceDict[key] = round(sumCounted[key]/sum,4)
print(sumFrequenceDict)
sumFrequenceDict = sorted(sumFrequenceDict.items(), key=lambda item: item[0])
print(sumFrequenceDict)
sum = 0
sumDict = dict()
for key in sumFrequenceDict:
    sum += key[1]
    sumDict[key[0]] = sum
print(sumDict)
sumFrequenceProb = []
for key in sumDict:
    sumFrequenceProb.append(sumDict[key])
print(sumFrequenceProb)


# counted = Counter(frequenceList)
# print(counted)
# sum = 0
#
# for key in counted:
#     sum += counted[key]
# print(sum)
# frequenceDict = dict()
# for key in counted:
#     frequenceDict[key] = round(counted[key]/sum,4)
# frequenceDict = sorted(frequenceDict.items(), key=lambda item: item[0])
# print(frequenceDict)
# sum = 0
# sumDict = dict()
# for key in frequenceDict:
#     sum += key[1]
#     sumDict[key[0]] = sum
# print(sumDict)
# # sumDict = sorted(sumDict.items(), key=lambda item: item[0])
# # print(sumDict)
#
# frequenceProb = []
# for key in sumDict:
#     frequenceProb.append(sumDict[key])
# print(frequenceProb)
# # plt.hist(frequenceList,[1,2,3,4,5,6,7,8,9,10,11,12],density=True)
# # # plt.xlabel(Xlabel)
# # plt.xlim(0,13)
# # # plt.ylabel(Ylabel)
# # # plt.ylim(Ymin,Ymax)
# # # plt.title(Title)
# # plt.show()