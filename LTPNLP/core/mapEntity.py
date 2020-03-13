# -*- coding: utf-8 -*-

def mapEntity(triple_list,all_entity):
    outputTriple = []
    for tripleSet in triple_list:
        for triple in tripleSet:
            subject = triple[0]
            object = triple[2]
            if subject in all_entity and object in all_entity:
                outputTriple.append(triple)
    return outputTriple

def mapEntityForSet(triple_list,all_entity):
    outputTriple = []
    for triple in triple_list:
        subject = triple[0]
        object = triple[2]
        if subject in all_entity and object in all_entity:
            outputTriple.append(triple)
    return outputTriple



def removeTheSame2(triple_list):
    outputTriple = []
    subList = []
    objList = []
    SameTriple = []
    for triple in triple_list:
        if len(triple[1]) == 2:
            tripleNew1 = []
            tripleNew1.append(triple[0])
            tripleNew1.append(triple[1][0])
            tripleNew1.append(triple[2])

            tripleNew2 = []
            tripleNew2.append(triple[0])
            tripleNew2.append(triple[1][1])
            tripleNew2.append(triple[2])

            if hasTriple(tripleNew1,triple_list) and hasTriple(tripleNew2,triple_list):
                print(tripleNew1)
                print(tripleNew2)
                SameTriple.append(tripleNew1)
                SameTriple.append(tripleNew2)
                continue
        if len(triple[1]) == 3:
            tripleNew1 = []
            tripleNew1.append(triple[0])
            tripleNew1.append(triple[1][0])
            tripleNew1.append(triple[2])

            tripleNew2 = []
            tripleNew2.append(triple[0])
            tripleNew2.append(triple[1][1]+""+triple[1][2])
            tripleNew2.append(triple[2])

            tripleNew3 = []
            tripleNew3.append(triple[0])
            tripleNew3.append(triple[1][0]+""+triple[1][1])
            tripleNew3.append(triple[2])

            tripleNew4 = []
            tripleNew4.append(triple[0])
            tripleNew4.append(triple[1][2])
            tripleNew4.append(triple[2])


            if hasTriple(tripleNew1,triple_list) and hasTriple(tripleNew2,triple_list):
                print(tripleNew1)
                print(tripleNew2)
                SameTriple.append(tripleNew1)
                SameTriple.append(tripleNew2)
                continue

            elif hasTriple(tripleNew3,triple_list) and hasTriple(tripleNew4,triple_list):
                print(tripleNew3)
                print(tripleNew4)
                SameTriple.append(tripleNew3)
                SameTriple.append(tripleNew4)
                continue
    if len(SameTriple) != 0:
        # tripleNew1 = SameTriple[0]
        # tripleNew2 = SameTriple[1]


        for triple in triple_list:
            flag = False
            for tripleNew in SameTriple:
                if tripleNew[0] == triple[0] and tripleNew[1] == triple[1] and tripleNew[2] == triple[2]:
                    flag = True
            if flag == False:
                outputTriple.append(triple)
        return outputTriple
    else:
        for triple in triple_list:
            outputTriple.append(triple)
        return outputTriple

def hasTriple(triple,triple_list):
    for tripleNew in triple_list:
        if tripleNew[0] == triple[0] and tripleNew[1] == triple[1] and tripleNew[2] == triple[2]:
            return True
    return False

def getAttWord():
    attWord = []
    for line in open("..\\source\\中文职务名词.txt",'r',encoding='UTF-8'):  # 设置文件对象并读取每一行文件
        attWord.append(line.strip('\n'))
    return attWord

if __name__ == "__main__":
    triple_list = [["和珅","留","嘉乐堂诗集"],["和珅","有","嘉乐堂诗集"],["和珅","留有","嘉乐堂诗集"],["和珅","哈哈哈","嘉乐堂诗集"]]
    print(removeTheSame2(triple_list))