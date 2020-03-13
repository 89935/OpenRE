import json
import csv
import thulac
f = open("..\\entity_verb_result\\name_place_organization_classification_v5.json","r",encoding="utf-8")
file = f.read()
person_entity = json.loads(file)['人--412']
location_entity = json.loads(file)['地点--500']
organization_entity = json.loads(file)['组织机构--71']
f.close()
print(person_entity)
print(location_entity)
print(organization_entity)

thu1 = thulac.thulac()
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
sFileName='..//entity_verb_result//intersection_only_verb_windowWord_1_beforeAndAfter.csv'

if __name__ == "__main__":
    allRel = []
    num = 0  # or 3 限制了关系在上下文所出现的频数的要求，设置为0时，则不限制
    with open(sFileName,newline='',encoding='UTF-8') as csvfile:
        loc_loc_triples =dict()
        loc_per_triples =dict()
        loc_org_triples =dict()
        per_per_triples =dict()
        per_org_triples =dict()
        org_org_triples =dict()
        rows=csv.reader(csvfile)
        all_entity = []
        for row in rows:
            # print(row)
            all_entity = row
            break
        count = 0
        for row in rows:
            count = count+1
            if row[0] in location_entity:
                per_triples = []
                loc_triples = []
                org_triples = []
                for i in range(1,count):
                    if len(row[i])>2:
                        line = []
                        line.append(row[0])
                        line.append(all_entity[i])
                        # line.append(row[i])
                        newList = []
                        relList = eval(row[i])  # [('收藏_v', [1, 2]), ('兴建_v', [1, 1]), ('成为_v', [1, 1]), ('包含_v', [1, 1]), ('修建_v', [1, 1])]

                        for rel in relList:  # ('收藏_v', [1, 2])
                            rel_v = rel[0]  # '收藏_v'
                            freq = rel[1]  # [1,2]
                            if freq[0]>=num and freq[1]>= num:  # 限制了关系出现的频数要求
                                rel_word = rel_v.split('_v')[0]  # 收藏
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
                    loc_loc_triples[row[0]] =loc_triples
                if len(per_triples)!= 0:
                    loc_per_triples[row[0]] = per_triples
                if len(org_triples)!= 0:
                    loc_org_triples[row[0]] = org_triples
            if row[0] in person_entity:
                per_triples = []
                org_triples = []
                for i in range(1,count):
                    if len(row[i])>2:
                        line = []
                        line.append(row[0])
                        line.append(all_entity[i])
                        newList = []
                        relList = eval(row[i])  # [('收藏_v', [1, 2]), ('兴建_v', [1, 1]), ('成为_v', [1, 1]), ('包含_v', [1, 1]), ('修建_v', [1, 1])]
                        for rel in relList:  # ('收藏_v', [1, 2])
                            rel_v = rel[0]  # '收藏_v'
                            freq = rel[1]  # [1,2]
                            if freq[0] >= num and freq[1] >= num:
                                rel_word = rel_v.split('_v')[0]  # 收藏
                                if thulacFilter(rel_word) == True:
                                    allRel.append(rel_word)
                                    newList.append(rel)
                        if len(newList) == 0:
                            continue
                        line.append(newList)
                        # print(row[i])
                        if all_entity[i] in person_entity:
                            per_triples.append(line)
                        if all_entity[i] in organization_entity:
                            org_triples.append(line)
                if len(per_triples)!= 0:
                    per_per_triples[row[0]] = per_triples
                if len(org_triples)!= 0:
                    per_org_triples[row[0]] = org_triples
            if row[0] in organization_entity:
                org_triples = []
                for i in range(1,count):
                    if len(row[i])>2:
                        line = []
                        line.append(row[0])
                        line.append(all_entity[i])
                        newList = []
                        relList = eval(row[i])  # [('收藏_v', [1, 2]), ('兴建_v', [1, 1]), ('成为_v', [1, 1]), ('包含_v', [1, 1]), ('修建_v', [1, 1])]
                        for rel in relList:  # ('收藏_v', [1, 2])
                            rel_v = rel[0]  # '收藏_v'
                            freq = rel[1]  # [1,2]
                            if freq[0] >= num and freq[1] >= num:
                                rel_word = rel_v.split('_v')[0]  # 收藏
                                if thulacFilter(rel_word) == True:
                                    # allRel.append(rel_word)
                                    newList.append(rel)
                        if len(newList) == 0:
                            continue
                        line.append(newList)
                        if all_entity[i] in organization_entity:
                            org_triples.append(line)
                if len(org_triples)!= 0:
                    per_org_triples[row[0]] = org_triples
    print(len(allRel))
    print(len(set(allRel)))
    with open('document-level-output/triples4/loc_loc_triples4.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_loc_triples, ensure_ascii=False))
    with open('document-level-output/triples4/loc_per_triples4.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_per_triples, ensure_ascii=False))
    with open('document-level-output/triples4/loc_org_triples4.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(loc_org_triples, ensure_ascii=False))
    with open('document-level-output/triples4/per_per_triples4.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_per_triples, ensure_ascii=False))
    with open('document-level-output/triples4/per_org_triples4.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(per_org_triples, ensure_ascii=False))
    with open('document-level-output/triples4/org_org_triples4.json', 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(org_org_triples, ensure_ascii=False))
        # print(location_triples)
    # print(all_line)
