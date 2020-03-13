import json
import re

def not_empty(s):
    return s and "".join(s.split())

def splitSentence(text):
    pattern = r'。|！|？|；|='
    result_list = re.split(pattern, text)
    result_list = list(filter(not_empty, result_list))
    #    print(result_list)
    return result_list


def occurrence(sentence_list, entity1, entity2):
    result_list = []
    for sentence in sentence_list:
        if entity1 in sentence and entity2 in sentence:
            result_list.append(sentence)
    return result_list


if __name__ == "__main__":
    f = open('entity_verb_result\\' + "5A_北京故宫博物院.txt"
             , 'r', encoding='utf-8')
    file = f.read()
    #    print(file)
    json_file = list(file)  # 转化为json格式

    print(json_file)