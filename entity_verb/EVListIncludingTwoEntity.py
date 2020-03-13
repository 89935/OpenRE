import json
import csv
import os
def EVoccurrence(text,entity1,entity2):
    flag1 = False
    flag2 = False
    for item in text:
        word = item[0]
        location = word.find("_")
        Numlocation = word.find("#")
        word = word[Numlocation+1:location]
        if flag1==False:
            if entity1 == word:
                flag1 = True
        if flag2 == False:
            if entity2 == word:
                flag2 = True
        if flag1 and flag2:
            return text

def EVfrequence(text_list):
    EV_dict = dict()
    for text in text_list:
        for item in text :
            word = item[0]
            if 'v' in word:
                if word not in EV_dict:
                    EV_dict[word] = 1
                else:
                    EV_dict[word]+=1
            # location = word.find("_")
            # Numlocation = word.find("#")
            # word = word[Numlocation+1:location]
            # if word not in EV_dict:
            #     EV_dict[word] = 1
            # else:
            #     EV_dict[word]+=1
        # print(EV_dict)
    EV_dict = sorted(EV_dict.items(), key=lambda item: item[1],reverse=True)
    return EV_dict


if __name__ == "__main__":
    """获取all_entity"""
    f = open('entity_verb_result\\' + "all_entity.json"
             , 'r', encoding='utf-8')
    file = f.read()
    all_entity = json.loads(file)['all_entity']
    f.close()
    # print(all_entity)
    path = r"entity_verb_result\\json"

    file_list = os.listdir(path)
    json_file = []
    for file_name in file_list:
        print(file_name)
        f = open('entity_verb_result\\json\\' + file_name
                 , 'r', encoding='utf-8')

        for line in f.readlines():
            json_line = json.loads(line)
            for key in json_line:
                json_file.append(json_line.get(key))
    print(json_file)
    # EV_list = []
    # entity1 = "故宫"
    # entity2 = "乾隆"
    all_entity = ["中和殿","外朝"]
    all_entity_intersection = []
    row1 = [" "]
    for entity in all_entity:
        row1.append(entity)
    all_entity_intersection.append(row1)

    for entity1 in all_entity:
        entity1_list = [entity1]
        for entity2 in all_entity:
            sentenceIncluding_list_list = []
            for line in json_file:
                sentenceIncluding_list = EVoccurrence(line, entity1, entity2)
                if sentenceIncluding_list!= None:
                    print(sentenceIncluding_list)
                    sentenceIncluding_list_list.append(sentenceIncluding_list)
                        # print(EVfrequence(sentenceIncluding_list))

            one_intersection = EVfrequence(sentenceIncluding_list_list)
            entity1_list.append(one_intersection)
        all_entity_intersection.append(entity1_list)
    # with open('entity_verb_result\\两个实体在一个句子中共现的Entity_Verb_only_verb.csv', 'w', newline='', encoding="utf-8") as t_file:
    #     csv_writer = csv.writer(t_file)
    #     for l in all_entity_intersection:
    #         csv_writer.writerow(l)
    # for json in json_file:
    #     text = json_file.get(key)  # 读取text
    #
