import json
import csv
import thulac
f = open("../entity_verb_result/name_place_organization_classification_人工修正版.json", "r", encoding="utf-8")  # 1、修改为分类结果文件，即name_place_organization_classification的输出文件
file = f.read()
person_entity = json.loads(file)['人--412']  # 2、修改为json文件中“人物”实体列表所对应的key
location_entity = json.loads(file)['地点--500']  # 3、修改为json文件中“地点”实体列表所对应的key
organization_entity = json.loads(file)['组织机构--71']  # 4、修改为json文件中组织机构实体列表所对应的key


print(person_entity)
print(len(person_entity))
print(location_entity)
print(len(location_entity))
print(organization_entity)
print(len(organization_entity))
entityCategoryDict = dict()
entityCategoryDict['person'] = person_entity
entityCategoryDict['location'] = location_entity
entityCategoryDict['organization'] = organization_entity

thu1 = thulac.thulac()
# sFileName='..//..//entity_verb_result//intersection_only_verb_windowWord_1_v6_longestEntity_one_sentence_beforeAndAfter.csv'  # 5、伴随词的交集文件，修改为entityContextUnion_only_verb_beforeAndAfter.py输出的csv文件


def thulacFilter(word):
    """
    通过THULAC来过滤关系是否为动词
    :param word:
    :return: True(该词是动词)，False(该词不是动词)
    """
    if len(thu1.cut(word)) == 1 and thu1.cut(word)[0][1] != 'v':  # 分词结果只有一个单词，且不为v
        return False
    elif len(thu1.cut(word)) == 1 and thu1.cut(word)[0][1] == 'v':  # 分词结果只有一个单词，且为v
        return True
    elif len(thu1.cut(word)) > 1:  # 分词结果中含有多个单词
        for word_pos in thu1.cut(word):
            if word_pos[1] == 'v':  # 只要有一个单词的词性标注为v
                return True
        return False  # 否则所有单词词性标注都不为v

def generateCategoryTriples(allTriplesList):
    loc_loc_triples,loc_per_triples,loc_org_triples = [],[],[]
    per_loc_triples,per_per_triples,per_org_triples = [],[],[]
    org_loc_triples,org_per_triples,org_org_triples = [],[],[]
    for tripe in allTriplesList:
        subject = tripe[0]
        relation = tripe[1]
        object = tripe[2]
        if thulacFilter(relation) == False:
            print(relation)
            continue
        else:
            if subject in location_entity:
                if object in location_entity:
                    loc_loc_triples.append(tripe)
                elif object in person_entity:
                    loc_per_triples.append(tripe)
                elif object in organization_entity:
                    loc_org_triples.append(tripe)
            if subject in person_entity:
                if object in location_entity:
                    per_loc_triples.append(tripe)
                elif object in person_entity:
                    per_per_triples.append(tripe)
                elif object in organization_entity:
                    per_org_triples.append(tripe)
            if subject in organization_entity:
                if object in location_entity:
                    org_loc_triples.append(tripe)
                elif object in person_entity:
                    org_per_triples.append(tripe)
                elif object in organization_entity:
                    org_org_triples.append(tripe)

    return loc_loc_triples, loc_per_triples, loc_org_triples ,per_loc_triples,\
           per_per_triples, per_org_triples ,org_loc_triples, org_per_triples, org_org_triples



if __name__ == "__main__":
    f = open('sentence_level2_result\\V0.4\\' + 'allTripes.json', 'r', encoding='utf-8')
    allTriplesList = []

    for line in f.readlines():
        json_line = json.loads(line)
        for key in json_line:
            for tripe in json_line.get(key):
                allTriplesList.append(tripe)
    print(allTriplesList)
    print(len(allTriplesList))
    loc_loc_triples,loc_per_triples,loc_org_triples ,per_loc_triples,per_per_triples,\
    per_org_triples,org_loc_triples,org_per_triples,org_org_triples = generateCategoryTriples(allTriplesList)
    print(len(loc_loc_triples))
    print(len(loc_per_triples))
    print(len(loc_org_triples))
    print(len(per_loc_triples))
    print(len(per_per_triples))
    print(len(per_org_triples))
    print(len(org_loc_triples))
    print(len(org_per_triples))
    print(len(org_org_triples))
    # allRel = []
    #
    # num = 0  # 6、限制了关系在上下文所出现次数的要求，设置为0时，则不限制，若=3，则限制该关系词至少在该实体的上下文中出现3次
    # loc_loc_triples,loc_per_triples,loc_org_triples = generateCategoryTriples("location",num)
    # per_loc_triples,per_per_triples,per_org_triples = generateCategoryTriples("person",num)
    # org_loc_triples,org_per_triples,org_org_triples = generateCategoryTriples("organization",num)


    tripleName = ''  # 7、只是为了给输出的文件赋予一个唯一的名字
    fileLocation = 'sentence_level2_result\\V0.3\\'
    with open(fileLocation+'loc_loc_triples'+tripleName+'.json', 'w',  # 9、修改loc_loc三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_loc_triples, ensure_ascii=False))
    with open(fileLocation+'loc_per_triples'+tripleName+'.json', 'w',  # 9、修改loc_per三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_per_triples, ensure_ascii=False))
    with open(fileLocation+'loc_org_triples'+tripleName+'.json', 'w',  # 10、修改loc_org三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_org_triples, ensure_ascii=False))
    with open(fileLocation+'per_loc_triples'+tripleName+'.json', 'w',  # 11、修改per_loc三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_loc_triples, ensure_ascii=False))
    with open(fileLocation+'per_per_triples'+tripleName+'.json', 'w',  # 12、修改per_per三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_per_triples, ensure_ascii=False))
    with open(fileLocation+'per_org_triples'+tripleName+'.json', 'w',  # 13、修改per_org三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_org_triples, ensure_ascii=False))
    with open(fileLocation+'org_loc_triples'+tripleName+'.json', 'w',  # 14、修改org_loc三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(org_loc_triples, ensure_ascii=False))
    with open(fileLocation+'org_per_triples'+tripleName+'.json', 'w',  # 15、修改org_per三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(org_per_triples, ensure_ascii=False))
    with open(fileLocation+'org_org_triples'+tripleName+'.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(org_org_triples, ensure_ascii=False))


        # print(location_triples)
    # print(all_line)
