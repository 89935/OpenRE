import json

f = open('sentence_level2_result\\' + "jieba+LTP额外补充的命名实体长度大于1.json", 'r', encoding='utf-8')
file = f.read()
f.close()
additional_entity_postag = json.loads(file)
entityList = []
personList = []
locationList = []
organizationList = []
for entity_postag in additional_entity_postag:
    entity = entity_postag.split('---')[0]
    postag = entity_postag.split('---')[1]
    if postag == 'ni':
        organizationList.append(entity)
    elif postag == 'nh':
        personList.append(entity)
    elif postag == 'ns':
        locationList.append(entity)
    entityList.append(entity)
print(entityList)
print(personList)
print(locationList)
print(organizationList)

outputDict = dict()
outputDict['人物'] = personList
outputDict['地点'] = locationList
outputDict['组织机构'] = organizationList
print(len(personList))
print(len(locationList))
print(len(organizationList))


with open('sentence_level2_result\\' + "额外补充长度大于1实体分类结果.json", 'w',  # 6、替换您输出分类结果的文件名
          encoding='utf-8') as json_file:
    json_file.write(json.dumps(outputDict, ensure_ascii=False))