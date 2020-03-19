"""
从一个句子中，根据得到的EVList，挑选出名词实体对，并给名词实体对中塞动词
实体对中两个实体的距离不能超过10，之间不能包含其他实体
也要满足约束1和约束2

"""
import json
import thulac

f = open("../entity_verb_result/all_entity.json", "r", encoding="utf-8")
file = f.read()
all_entity = json.loads(file)['all_entity']
f.close()

f = open("../entity_verb_result/name_place_organization_classification_人工修正版.json", "r",
         encoding="utf-8")  # 1、修改为分类结果文件，即name_place_organization_classification的输出文件
file = f.read()
person_entity = json.loads(file)['人--412']  # 2、修改为json文件中“人物”实体列表所对应的key
location_entity = json.loads(file)['地点--500']  # 3、修改为json文件中“地点”实体列表所对应的key
organization_entity = json.loads(file)['组织机构--71']  # 4、修改为json文件中组织机构实体列表所对应的key
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

loc_loc_triples, loc_per_triples, loc_org_triples, loc_time_triples = [], [], [], []
per_loc_triples, per_per_triples, per_org_triples, per_time_triples = [], [], [], []
org_loc_triples, org_per_triples, org_org_triples, org_time_triples = [], [], [], []
time_loc_triples, time_per_triples, time_org_triples = [], [], []

thu1 = thulac.thulac()


def getNounAndVerbInSentence(sentence):
    nounList = []
    verbList = []
    for item in sentence:
        word = item[0]
        location = word.find("_")
        numLocation = word.find("#")
        clean_word = word[numLocation + 1:location]
        if numLocation == -1:
            verbList.append(clean_word)
        if numLocation != -1:
            nounList.append(clean_word)
    return nounList, verbList


def judgeCate(wordItem):
    word = wordItem[0]
    location = word.find("_")
    numLocation = word.find("#")
    clean_word = word[numLocation + 1:location]
    clean_word_pos = 'NULL'
    if clean_word in all_entity:  # xlore分类的元素不会重复
        if clean_word in organization_entity:
            clean_word_pos = 'ORG'
        if clean_word in person_entity:
            clean_word_pos = 'PER'
        if clean_word in location_entity:
            clean_word_pos = 'LOC'
    else:
        print('???' + word)
        if 'ns' in word:
            clean_word_pos = 'LOC'
        if 'ni' in word:
            clean_word_pos = 'ORG'
        if 'nh' in word:
            clean_word_pos = 'PER'
        if 'tempNoun' in word:
            clean_word_pos = 'NT'
    return clean_word_pos


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


def generateCandidateTriples(sentence, rawSentence):
    triplesList = []
    verbList = []
    for item in sentence:
        word = item[0]
        location = word.find("_")
        numLocation = word.find("#")
        clean_word = word[numLocation + 1:location]
        if numLocation == -1:
            verbList.append(item[1])  # 存储动词位置列表

    for item in sentence:
        word = item[0]
        wordLocation = item[1]
        tagLocation = word.find("_")
        numLocation = word.find("#")
        clean_word = word[numLocation + 1:tagLocation]
        # triple = []
        # triple.append(clean_word)
        objectList = []
        if numLocation == -1:  # 找主语，不考虑动词
            continue

        for otherItem in sentence:
            otherWord = otherItem[0]
            otherWordLocation = otherItem[1]
            otherTagLocation = otherWord.find("_")
            otherNumLocation = otherWord.find("#")
            otherClean_word = otherWord[otherNumLocation + 1:otherTagLocation]
            if otherWordLocation <= wordLocation:
                continue

            elif otherWordLocation - wordLocation > 10:  # 两个实体之间的距离不能超过10
                break

            else:
                if otherNumLocation != -1:  # 如果该词是一个实体的话
                    objectList.append(otherItem)
                    """
                    这里设置的1表明，一个实体对中的两个实体之间不能包含有其他实体，所以一个主语所对应的宾语最多只能有一个；
                    若设置为2则表明，一个实体对中的两个实体之间最多有一个其他实体，所以一个主语对应的宾语可以有两个；
                    当然这些的前提是，宾语必须在主语之后，而且主语与宾语的距离不超过10
                    """
                    if len(objectList) == 1:
                        break

        for objectItem in objectList:
            objectWord = objectItem[0]
            objectWordLocation = objectItem[1]
            objectTagLocation = objectWord.find("_")
            objectNumLocation = objectWord.find("#")
            objectClean_word = objectWord[objectNumLocation + 1:objectTagLocation]

            for verbItem in sentence:
                verbWord = verbItem[0]
                verbWordLocation = verbItem[1]
                verbTagLocation = verbWord.find("_")
                verbNumLocation = verbWord.find("#")
                verbClean_word = verbWord[verbNumLocation + 1:verbTagLocation]
                if verbWordLocation <= wordLocation:  # 动词要在主语之后
                    continue

                elif verbWordLocation >= objectWordLocation:  # 动词要在宾语之前
                    break

                else:
                    if verbNumLocation == -1:
                        nextObjectWordLocation = objectWordLocation + len(objectClean_word)
                        if nextObjectWordLocation < len(rawSentence):
                            if rawSentence[nextObjectWordLocation] == '的':  # 约束2：原句中宾语的后一个字不能是“的”
                                print(rawSentence)
                                print('!!!' + str(objectItem))
                                continue
                            if nextObjectWordLocation in verbList:  # 约束1：原句中宾语的后一个词不能是动词
                                print(rawSentence)
                                print('!!!' + str(objectItem))
                                continue

                        triple = []
                        triple.append(clean_word)
                        triple.append(verbClean_word)
                        triple.append(objectClean_word)
                        triplesList.append(triple)
                        if thulacFilter(verbClean_word) == False:
                            continue
                        subjectCat = judgeCate(item)
                        objectCat = judgeCate(objectItem)
                        if subjectCat == 'LOC':
                            if objectCat == 'LOC':
                                loc_loc_triples.append(triple)
                            if objectCat == 'PER':
                                loc_per_triples.append(triple)
                            if objectCat == 'ORG':
                                loc_org_triples.append(triple)
                            if objectCat == 'NT':
                                loc_time_triples.append(triple)
                        if subjectCat == 'PER':
                            if objectCat == 'LOC':
                                per_loc_triples.append(triple)
                            if objectCat == 'PER':
                                per_per_triples.append(triple)
                            if objectCat == 'ORG':
                                per_org_triples.append(triple)
                            if objectCat == 'NT':
                                per_time_triples.append(triple)
                        if subjectCat == 'ORG':
                            if objectCat == 'LOC':
                                org_loc_triples.append(triple)
                            if objectCat == 'PER':
                                org_per_triples.append(triple)
                            if objectCat == 'ORG':
                                org_org_triples.append(triple)
                            if objectCat == 'NT':
                                org_time_triples.append(triple)
                        if subjectCat == 'NT':
                            if objectCat == 'LOC':
                                time_loc_triples.append(triple)
                            if objectCat == 'PER':
                                time_per_triples.append(triple)
                            if objectCat == 'ORG':
                                time_org_triples.append(triple)

    return triplesList


json_file = []
file_name = "all_只包含最长实体.json"
print(file_name)
f = open('sentence_level2_result\\V0.5\\' + file_name, 'r', encoding='utf-8')
rawSentenceList = []
for line in f.readlines():
    json_line = json.loads(line)
    for key in json_line:
        rawSentenceList.append(key)
        json_file.append(json_line.get(key))
print(json_file)
f.close()
print(json_file)
print(rawSentenceList)
allTripes = []
for sentence,rawSentence in zip(json_file,rawSentenceList):
    triplesList = generateCandidateTriples(sentence,rawSentence)
    if len(triplesList)!=0:
        print(sentence)
        print(triplesList)
        for tripe in triplesList:
            allTripes.append(tripe)
print(allTripes)
print("所有三元组的个数")
print(len(allTripes))

# f = open('sentence_level2_result\\V0.5\\allTripes.json', 'w', encoding='utf-8')
# for sentence, rawSentence in zip(json_file, rawSentenceList):
#     triplesList = generateCandidateTriples(sentence, rawSentence)
#     line_dict = dict()
#     if len(triplesList) != 0:
#         line_dict[rawSentence] = triplesList
#         f.write(json.dumps(line_dict, ensure_ascii=False) + '\n')
#
# f.close()

print(loc_loc_triples)
print(len(loc_loc_triples))
print(loc_per_triples)
print(len(loc_per_triples))
print(loc_org_triples)
print(len(loc_org_triples))

print(per_loc_triples)
print(len(per_loc_triples))

print(per_per_triples)
print(len(per_per_triples))
print(per_org_triples)
print(len(per_org_triples))

print(org_loc_triples)
print(len(org_loc_triples))
print(org_per_triples)
print(len(org_per_triples))
print(org_org_triples)
print(len(org_org_triples))

print(per_time_triples)
print(len(per_time_triples))
print(loc_time_triples)
print(len(loc_time_triples))
print(org_time_triples)
print(len(org_time_triples))
print(time_loc_triples)
print(len(time_loc_triples))
print(time_per_triples)
print(len(time_per_triples))
print(time_org_triples)
print(len(time_org_triples))

tripleName = ''  # 7、只是为了给输出的文件赋予一个唯一的名字
fileLocation = 'sentence_level2_result\\V0.5\\'
with open(fileLocation + 'loc_loc_triples' + tripleName + '.json', 'w',  # 9、修改loc_loc三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(loc_loc_triples, ensure_ascii=False))
with open(fileLocation + 'loc_per_triples' + tripleName + '.json', 'w',  # 9、修改loc_per三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(loc_per_triples, ensure_ascii=False))
with open(fileLocation + 'loc_org_triples' + tripleName + '.json', 'w',  # 10、修改loc_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(loc_org_triples, ensure_ascii=False))
with open(fileLocation + 'per_loc_triples' + tripleName + '.json', 'w',  # 11、修改per_loc三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(per_loc_triples, ensure_ascii=False))
with open(fileLocation + 'per_per_triples' + tripleName + '.json', 'w',  # 12、修改per_per三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(per_per_triples, ensure_ascii=False))
with open(fileLocation + 'per_org_triples' + tripleName + '.json', 'w',  # 13、修改per_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(per_org_triples, ensure_ascii=False))
with open(fileLocation + 'org_loc_triples' + tripleName + '.json', 'w',  # 14、修改org_loc三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(org_loc_triples, ensure_ascii=False))
with open(fileLocation + 'org_per_triples' + tripleName + '.json', 'w',  # 15、修改org_per三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(org_per_triples, ensure_ascii=False))
with open(fileLocation + 'org_org_triples' + tripleName + '.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(org_org_triples, ensure_ascii=False))

with open(fileLocation + 'org_org_triples' + tripleName + '.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(org_org_triples, ensure_ascii=False))

# ------------------------------------------------
with open(fileLocation + 'loc_time_triples' + tripleName + '.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(loc_time_triples, ensure_ascii=False))

with open(fileLocation + 'per_time_triples' + tripleName + '.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(per_time_triples, ensure_ascii=False))

with open(fileLocation + 'org_time_triples' + tripleName + '.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(org_time_triples, ensure_ascii=False))

with open(fileLocation + 'time_loc_triples' + tripleName + '.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(time_loc_triples, ensure_ascii=False))

with open(fileLocation + 'time_per_triples' + tripleName + '.json', 'w',  # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(time_per_triples, ensure_ascii=False))

with open(fileLocation + 'time_org_triples' + tripleName + '.json', 'w',
          # 16、修改org_org三元组的存储路径和文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(time_org_triples, ensure_ascii=False))

    # nounList,verbList = getNounAndVerbInSentence(sentence)
    # print(sentence)
    # print(nounList)
    # print(verbList)
