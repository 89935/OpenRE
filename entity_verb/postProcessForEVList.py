import json
fileList = ['5A_北京故宫博物院.json', '5A_天坛公园.json','5A_恭王府.json','5A_颐和园.json','5A_慕田峪长城.json']
json_file = []
for file_name in fileList:
    print(file_name)
    f = open('entity_verb_result\\实体+额外名词+jieba分词+时间名词\\' + file_name, 'r', encoding='utf-8')
    for line in f.readlines():
        json_line = json.loads(line)
        for key in json_line:
            json_file.append(json_line.get(key))
print(json_file)

newEVList = []
for EVList in json_file:
    print(EVList)
    EVListHelp = EVList[:]  # 建立一个help列表，帮助循环
    for item in EVListHelp:
        if item not in EVList:  # 若EVListHelp中的该项不存在EVList中（即，该项已删除，则不进行下列操作）
            continue
        print(item)
        word = item[0]
        position = item[1]
        if '#' in word:  # 如果该单词是一个实体
            location = word.find("_")
            Numlocation = word.find("#")
            clean_word = word[Numlocation + 1:location]
            print("----------------out Loop------------------")
            print(clean_word)
            leftRange = position
            rightRange = position + len(clean_word) - 1
            print(leftRange,rightRange)
            for otherItem in EVListHelp:
                if otherItem not in EVList:  # 若EVListHelp中的该项不存在EVList中（即，该项已删除，则不进行下列操作），以防删除的元素不在EVList里
                    continue
                otherWord = otherItem[0]
                otherPosition = otherItem[1]
                if '#' in otherWord:  # 如果该单词是一个实体
                    location = otherWord.find("_")
                    Numlocation = otherWord.find("#")
                    clean_word = otherWord[Numlocation + 1:location]

                    otherLeftRange = otherPosition
                    otherRightRange = otherPosition + len(clean_word) - 1
                    if otherLeftRange==leftRange and otherRightRange ==rightRange:
                        continue
                    if otherLeftRange>=leftRange and otherRightRange <=rightRange:
                        print("---------Entity Inner Loop-----------------")
                        print(clean_word)
                        print(otherLeftRange, otherRightRange)
                        EVList.remove(otherItem)  # 对EVList里的该元素进行删除
                    else:
                        continue
                elif 'v' in otherWord:  # 如果该单词不是一个实体，而且是一个动词
                    location = otherWord.find("_")
                    Numlocation = otherWord.find("#")
                    clean_word = otherWord[Numlocation + 1:location]

                    otherLeftRange = otherPosition
                    otherRightRange = otherPosition + len(clean_word) - 1
                    if otherLeftRange==leftRange and otherRightRange ==rightRange:
                        continue
                    """
                    与对实体的处理相比：如果该动词和该实体，leftRange和rightRange都一样时，需要删除该动词，因为是对把实体分类为了动词
                    """
                    if otherLeftRange>=leftRange and otherRightRange <=rightRange:
                        print("---------Verb Inner Loop-----------------")
                        print(clean_word)
                        print(otherLeftRange, otherRightRange)
                        EVList.remove(otherItem)  # 对EVList里的该元素进行删除
                    else:
                        continue
    print(EVList)
    newEVList.append(EVList)

with open('entity_verb_result\\实体+额外名词+jieba分词+时间名词\\all_只包含最长实体.json', 'w',
          encoding='utf-8') as json_file:
    i = -1
    for line in newEVList:
        i += 1
        line_dict = dict()
        if len(line) != 0:
            line_dict[i] = line
            json_file.write(json.dumps(line_dict, ensure_ascii=False) + '\n')