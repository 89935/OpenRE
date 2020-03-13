import os
import json
if __name__ == "__main__":
    # 读取文件
    path = r"D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel"
    file_list = os.listdir(path)
    all_entity = []
    for file_name in file_list:
        print(file_name)
        f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\' + file_name
                 , 'r', encoding='utf-8')
        file = f.read()
        json_file = json.loads(file)  # 转化为json格式
        bdlink_entity = json_file.get("bdlink_entity")  # 读取bdlink_entity的数据
        xlink_entity = json_file.get("xlink_result") #读取xlink_entity的数据
        one_file_entity = []

        for entity in bdlink_entity:
            if(entity[0]!=None):
                one_file_entity.append(entity[0])
        for entity in xlink_entity:
            if(entity["label"]!=None):
                one_file_entity.append(entity["label"])
        print(one_file_entity)
        for one in one_file_entity:
            all_entity.append(one)
        f.close()
    all_entity_tuple = set(all_entity)
    all_entity_dic = dict()
    all_entity_dic["all_entity"] = list(all_entity_tuple)
    print(len(all_entity_tuple))
    # with open('entity_verb_result\\' + "all_entity.json", 'w',
    #           encoding='utf-8') as file:
    #     file.write(json.dumps(all_entity_dic,ensure_ascii=False))
    # with open('source\\' + "user.txt", 'w',
    #           encoding='utf-8') as file:
    #     entity_list = all_entity_dic["all_entity"]
    #     for i in entity_list:
    #         file.write(i+'\n')