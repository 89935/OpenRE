import json
# f = open("entity_verb_result\\all_entity_classification.json","r",encoding="utf-8")
f = open("entity_verb_result\\set_all_entity_classification.json","r",encoding="utf-8")  # 5、替换您在entityClassificationByXlore.py输出的文件名
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

    nameTagList = ["人物"]  # 人物类别的标签
    locTagList = ["地点","景点","建筑","旅游","城市","地理","行政区划","国家","地形地貌"]  # 地点类别的标签
    orgTagList = ["机构","学校","高校","公司","组织机构"]  # 组织机构类别的标签
    tagList = all_entity[i]

    # 23-29行的代码，可能会出现某一个实体在多个类别中
    # for tag in tagList:
    #     if tag in nameTagList:
    #         name_list.append(i)
    #     if tag in locTagList:
    #         place_list.append(i)
    #     if tag in orgTagList:
    #         organization_list.append(i)


    # 下面的代码，每个实体都只被分在一个类别中，不会出现不同的类别中出现相同的实体
    for tag in tagList:
        if tag in nameTagList:  # 如果实体标签中 存在上述 人物 分类标签，给人物投一票
            nameFlag +=1
        if tag in locTagList:  # 如果实体标签中 存在上述 地点 分类标签，给地点投一票
            locFlag +=1
        if tag in orgTagList:  # 如果实体标签中 存在 组织机构 分类标签，给 组织机构 投一票
            orgFlag +=1
    if nameFlag > locFlag and nameFlag > orgFlag:  # 如果人物票数最多，则把该词分为“人物”
        name_list.append(i)
    elif locFlag>nameFlag and locFlag>orgFlag:  # 如果地点票数最多，则把该词分为“地点”
        place_list.append(i)
    elif orgFlag > nameFlag and orgFlag > locFlag:  # 如果组织机构票数最多，则把该词分为“组织机构”
        organization_list.append(i)
    elif nameFlag>0 or locFlag>0 or orgFlag>0:  # 如果该实体存在两个分类或三个分类的票数一样多，且都大于0
        if nameFlag == locFlag :  # 如果人物和地点的分类票数一样多，把实体分为地点
            place_list.append(i)
        elif locFlag == orgFlag:  # 如果组织机构和地点的分类票数一样多，把实体分为地点
            place_list.append(i)
        elif nameFlag == orgFlag:  # 如果组织机构和人物的分类票数一样多，把实体分为人物
            name_list.append(i)



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
with open('entity_verb_result\\' + "name_place_organization_classification_v5.json", 'w',  # 6、替换您输出分类结果的文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(output_dict, ensure_ascii=False))