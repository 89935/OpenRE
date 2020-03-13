import json
import csv
import thulac
f = open("../../entity_verb_result/name_place_organization_classification_人工修正版.json", "r", encoding="utf-8")
file = f.read()
person_entity = json.loads(file)['人--412']
location_entity = json.loads(file)['地点--500']
organization_entity = json.loads(file)['组织机构--71']
f.close()
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
sFileName='..//..//entity_verb_result//intersection_only_verb_windowWord_1_v6_longestEntity_one_sentence_beforeAndAfter.csv'


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

# print(thulacFilter("造成损失"))
# print(thu1.cut("造成损失"))
# print(thulacFilter("恭王府外"))
# print(thu1.cut("恭王府外"))


# print(thulacFilter("造成位于"))
# print(thu1.cut("造成位于"))
#
#
# print(thulacFilter("建造于"))
# print(thu1.cut("建造于"))
#
# print(thulacFilter("北京故宫博物院"))
# print(thu1.cut("北京故宫博物院"))

def generateCategoryTriples(category,num):
    """
    从csv文件中生成指定实体对类别的三元组集合
    :param category: 指定实体对类别，person，location，organization
    :param num: 限制关系出现的频数要求
    :return: category_loc_triples,category_per_triples,category_org_triples
    """
    with open(sFileName, newline='', encoding='UTF-8') as csvfile:
        category_loc_triples = dict()
        category_per_triples = dict()
        category_org_triples = dict()
        rows = csv.reader(csvfile)
        all_entity = []
        for row in rows:
            # print(row)
            all_entity = row
            break
        count = 0
        for row in rows:
            count = count + 1
            if row[0] in entityCategoryDict[category]:
                per_triples = []
                loc_triples = []
                org_triples = []
                for i in range(1, len(all_entity)):  # 有顺序，需要考虑整个矩阵

                    if row[0]!=all_entity[i] and len(row[i]) > 2:
                        line = []
                        line.append(row[0])
                        line.append(all_entity[i])
                        # line.append(row[i])
                        newList = []
                        relList = eval(
                            row[i])  # [('陈设', [1, 2]), ('居住', [2, 1]), ('书', [1, 1]), ('位于', [1, 1]), ('生活', [1, 1])]

                        for rel in relList:  # ('陈设', [1, 2])
                            rel_v = rel[0]  # 陈设
                            freq = rel[1]  # [1,2]
                            if freq[0] >= num and freq[1] >= num:  # 限制了关系出现的频数要求
                                rel_word = rel_v  # 收藏
                                if thulacFilter(rel_word) == True:
                                    allRel.append(rel_word)
                                    newList.append(rel)
                                    print(rel)
                        if len(newList) == 0:
                            continue
                        line.append(newList)
                        if all_entity[i] in location_entity:
                            loc_triples.append(line)
                        if all_entity[i] in person_entity:
                            per_triples.append(line)
                        if all_entity[i] in organization_entity:
                            org_triples.append(line)
                if len(loc_triples) != 0:
                    category_loc_triples[row[0]] = loc_triples
                if len(per_triples) != 0:
                    category_per_triples[row[0]] = per_triples
                if len(org_triples) != 0:
                    category_org_triples[row[0]] = org_triples
    return category_loc_triples,category_per_triples,category_org_triples



if __name__ == "__main__":
    allRel = []
    num = 0  # or 3 限制了关系在上下文所出现的频数的要求，设置为0时，则不限制
    loc_loc_triples,loc_per_triples,loc_org_triples = generateCategoryTriples("location",num)
    per_loc_triples,per_per_triples,per_org_triples = generateCategoryTriples("person",num)
    org_loc_triples,org_per_triples,org_org_triples = generateCategoryTriples("organization",num)
    tripleName = '8'
    with open('../document-level-output/loc_loc_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_loc_triples, ensure_ascii=False))
    with open('../document-level-output/loc_per_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_per_triples, ensure_ascii=False))
    with open('../document-level-output/loc_org_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_org_triples, ensure_ascii=False))
    with open('../document-level-output/per_loc_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_loc_triples, ensure_ascii=False))
    with open('../document-level-output/per_per_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_per_triples, ensure_ascii=False))
    with open('../document-level-output/per_org_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_org_triples, ensure_ascii=False))
    with open('../document-level-output/org_loc_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(org_loc_triples, ensure_ascii=False))
    with open('../document-level-output/org_per_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(org_per_triples, ensure_ascii=False))
    with open('../document-level-output/org_org_triples'+tripleName+'.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(org_org_triples, ensure_ascii=False))
        # print(location_triples)
    # print(all_line)
