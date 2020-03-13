import json

def readAllEntity( file='entity_verb_result\\' + "all_entity.json"):
    f = open(file
             , 'r', encoding='utf-8')
    file = f.read()
    f.close()
    all_entity = json.loads(file)['all_entity']
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
    f = open("E:\\patch_tag.txt",'r',encoding='utf-8')
    xlorefile = f.read()
    count = 0
    allEntity = ['宋徽宗']
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
    all_entity = readAllEntity()
    entity_classification = classify(all_entity)
    # print(entity_classification)
    # with open('entity_verb_result\\' + "set_all_entity_classification.json", 'w',
    #           encoding='utf-8') as json_file:
    #     json_file.write(json.dumps(entity_classification,ensure_ascii=False))