import json
# f = open("entity_verb_result\\all_entity_classification.json","r",encoding="utf-8")
f = open("entity_verb_result\\set_all_entity_classification.json","r",encoding="utf-8")
file = f.read()
all_entity = json.loads(file)
f.close()
place_list = []
name_list = []
organization_list = []
output_dict = dict()
for i in all_entity:
    # print(i)
    nameFlag = 0
    locFlag = 0
    orgFlag = 0

    nameTagList = ["人物"]
    locTagList = ["地点","景点","建筑","旅游","城市","地理","行政区划","国家","地形地貌"]
    orgTagList = ["机构","学校","高校","公司","组织机构"]
    tagList = all_entity[i]
    for tag in tagList:
        if tag in nameTagList:
            nameFlag +=1
        if tag in locTagList:
            locFlag +=1
        if tag in orgTagList:
            orgFlag +=1
    if nameFlag > locFlag and nameFlag > orgFlag:
        name_list.append(i)
    elif locFlag>nameFlag and locFlag>orgFlag:
        place_list.append(i)
    elif orgFlag > nameFlag and orgFlag > locFlag:
        organization_list.append(i)
    elif nameFlag>0 or locFlag>0 or orgFlag>0:
        if nameFlag == locFlag :
            place_list.append(i)
        elif locFlag == orgFlag:
            place_list.append(i)
        elif nameFlag == orgFlag:
            name_list.append(i)
        else:
            print(i+str(nameFlag)+str(locFlag)+str(orgFlag))

f = open("source\\人物.txt","r",encoding="utf-8")
for line in f.readlines():
     line=line.strip('\n')
     name_list.append(line)
f.close()
print(name_list)

f = open("source\\地点.txt","r",encoding="utf-8")
for line in f.readlines():
     line=line.strip('\n')
     place_list.append(line)
f.close()
print(place_list)


f = open("source\\机构.txt","r",encoding="utf-8")
for line in f.readlines():
     line=line.strip('\n')
     organization_list.append(line)
f.close()
print(organization_list)




output_dict["人--"+str(len(name_list))] = name_list
print("人"+str(name_list))
output_dict["地点--"+str(len(place_list))] = place_list
print("地点"+str(place_list))
output_dict["组织机构--"+str(len(organization_list))] = organization_list
print("组织机构"+str(organization_list))

output_dict["人与地点的交集--"+str(len(list(set(name_list).intersection(set(place_list)))))] = list(set(name_list).intersection(set(place_list)))
print("人与地点的交集"+str(list(set(name_list).intersection(set(place_list)))))
output_dict["人与组织机构的交集--"+str(len(list(set(name_list).intersection(set(organization_list)))))] = list(set(name_list).intersection(set(organization_list)))
print("人与组织机构的交集"+str(list(set(name_list).intersection(set(organization_list)))))
output_dict["组织机构与地点的交集--"+str(len(list(set(place_list).intersection(set(organization_list)))))] = list(set(place_list).intersection(set(organization_list)))
print("组织机构与地点的交集"+str(list(set(place_list).intersection(set(organization_list)))))
output_dict["（人+地点+组织）分类的实体数/总实体数"] = len(set(set(name_list).union(set(place_list)).union(set(organization_list))))/len(all_entity)
print(len(set(set(name_list).union(set(place_list)).union(set(organization_list)))))
unprocessed = set(all_entity).difference(set(set(name_list).union(set(place_list)).union(set(organization_list))))
unprocessed_dict = dict()
for i in unprocessed:
    unprocessed_dict[i] = all_entity[i]
print(unprocessed_dict)
output_dict["未处理的实体--" + str(len(unprocessed_dict))] = unprocessed_dict
print(output_dict)
with open('entity_verb_result\\' + "name_place_organization_classification_v5.json", 'w',
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(output_dict, ensure_ascii=False))