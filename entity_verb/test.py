
def classify(allEntity):
    entity_classification = dict()
    f = open("E:\\patch_tag.txt",'r',encoding='utf-8')
    xlorefile = f.read()
    for entity in allEntity:
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
            # print(entityLine)
            entityName = entityLine.split("\t\t")[0]
            if "（" in entityName and entityName[-1]=="）":
                entityName = entityLine.split("（")[0]
            entityTag = entityLine.split("\t\t")[1]
            entityTag = entityTag.replace("::","")
            if entity == entityName:
                entityAllTag += entityTag+"||"
                print(entityLine)
            index+=len(entity)
        entity_classification[entity] = entityAllTag
    return entity_classification

if __name__ == "__main__":
    entity = ["水仙"]
    entity_classification = classify(entity)
    print(entity_classification)