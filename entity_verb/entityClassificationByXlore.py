import json

def readAllEntity( file):
    f = open(file
             , 'r', encoding='utf-8')
    file = f.read()
    f.close()
    all_entity = json.loads(file)['all_entity']  # 2、json文件中，所有实体的key值
    return all_entity

def readAllEntityInXlore():
    xloreEntityList = []
    f = open("E:\\patch_tag.txt",'r',encoding='utf-8')
    entityDict = dict()
    while True:
        line = f.readline()
        if not line:
            break
        entity = line.split("\t\t")[0]
        tag = line.split("\t\t")[1]
        tag = tag.replace("::","")
        tag = tag.strip()
        entityDict[entity] = tag
        xloreEntityList.append(line)
    f.close()
    with open("entity_verb_result\\xlore_entity.json", 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(entityDict, ensure_ascii=False) + '\n')
    return entityDict,xloreEntityList

def classify(allEntity):
    entity_classification = dict()
    length = len(allEntity)
    f = open("E:\\patch_tag.txt",'r',encoding='utf-8')  # 3、替换您的xlore所有实体的分类
    xlorefile = f.read()
    count = 0
    # allEntity = ['宋徽宗']
    for entity in allEntity:
        count +=1
        print(entity+"还剩"+str(length-count))
        index = 0
        entityAllTag = ""
        while index<len(xlorefile):
            index = xlorefile.find(entity, index)
            if index ==-1:
                break
            entityLine = ""
            position = index
            while xlorefile[position] != '\n':
                position -=1
            position += 1
            while xlorefile[position] != '\n':
                entityLine += xlorefile[position]
                position += 1
            entityName = entityLine.split("\t\t")[0]
            if "（" in entityName and entityName[-1]=="）":
                entityName = entityLine.split("（")[0]
            entityTag = entityLine.split("\t\t")[1]
            entityTag = entityTag.replace("::","")
            if entity == entityName:
                entityAllTag += entityTag+";"
            index+=len(entity)
        # entityAllTag = set(entityAllTag.split(";"))
        entity_classification[entity] = entityAllTag
        print(entity_classification)
    return entity_classification

if __name__ == "__main__":

    all_entity = readAllEntity('entity_verb_result\\' + "jieba+LTP额外补充的命名实体.json")  # 1、替换您的所有实体列表
    all_entity = ['厉先生']
    # f = open('entity_verb_result\\' + "jieba+LTP额外补充的命名实体.json", 'r', encoding='utf-8')
    # file = f.read()
    # f.close()
    # additional_entity_postag = json.loads(file)
    # entityList = []
    # for entity_postag in additional_entity_postag:
    #     entity = entity_postag.split('---')[0]
    #     entityList.append(entity)
    # print(entityList)
    entity_classification = classify(all_entity)
    print(entity_classification)
    # with open('entity_verb_result\\' + "额外补充实体的Xlore分类结果.json", 'w',  # 4、替换您输出的文件名
    #           encoding='utf-8') as json_file:
    #     json_file.write(json.dumps(entity_classification,ensure_ascii=False))