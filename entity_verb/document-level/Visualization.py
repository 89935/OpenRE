
import json

def readJsonToTriple(fileName):
    f = open('document-level-output\\' + fileName, 'r', encoding='utf-8')  # 2、修改为各个实体对类型的候选三元组文件所在的位置
    file = f.read()
    f.close()
    content = json.loads(file)  # 转化为json格式
    print(content)
    tripleList = []
    for key in content:
        entityPair = content[key]
        print(entityPair)
        for triple in entityPair:
            print(triple)
            for rel in triple[2]:
                tripleExample = []
                print(rel[0])
                rel_v = rel[0]
                relation = rel_v.split('_v')[0]
                print(relation)
                tripleExample.append(triple[0])
                tripleExample.append(relation)
                tripleExample.append(triple[1])
                print(tripleExample)
                tripleList.append(tripleExample)
    return tripleList

if __name__ == '__main__':
    fileList = ['loc_loc_triples9.json','loc_per_triples9.json','loc_org_triples9.json',
                'per_loc_triples9.json','per_per_triples9.json','per_org_triples9.json',
                'org_loc_triples9.json','org_per_triples9.json','org_org_triples9.json']  # 1、修改为step0_classifiedEntity_ForbeforeAndAfter所生成的各个实体对类型的候选三元组

    for fileName in fileList:
        tripleList = readJsonToTriple(fileName)
        file = r'C:\Users\thinkpad\Desktop\文档级进展\\' +fileName  # 3、输出文件的位置以及文件名
        with open(file, 'a+',encoding='utf-8') as f:
            for triple in tripleList:
                f.write(triple[0]+','+triple[1]+','+triple[2] + '\n')  # 加\n换行显示
        print(tripleList)
        for triple in tripleList:
            print(triple[0]+','+triple[1]+','+triple[2])
