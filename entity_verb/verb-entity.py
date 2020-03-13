# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:34:51 2019

@author: thinkpad
"""
import json
import re
import thulac
import os


def not_empty(s):
    return s and "".join(s.split())

def splitSentence(text):
    pattern = r'。|！|？|；|='
    result_list = re.split(pattern, text)
    result_list = list(filter(not_empty,result_list))
#    print(result_list)
    return result_list
    
def stopwordsList():
    """
    return:停用词列表
    """
    stop_list_Path = 'D:\python-file\\北京市旅游知识图谱\\verb-entity\\中文停用词.txt'
    f = open(stop_list_Path,'r',encoding='utf-8')
    stopwords = [line.strip() for line in f.readlines()]
#    print(stopwords)
    return stopwords

def splitWord(sentence_list,thu1):
    
    result_list = []
    stopwords = stopwordsList()
    
    for sentence in sentence_list:
        sentence = sentence.strip()
        result_words = []
        words = thu1.cut(sentence)  #进行一句话分词
        for word in words:
            if word[0] not in stopwords and len(word[0].strip())!=0:
                result_words.append(word)
        result_list.append(result_words)
#    print(result_list)
    return result_list

def getKeySentence(sentence_list,keyWords):
    result_list = []
    for sentence in sentence_list:
        for keyWord in keyWords:
            if keyWord in sentence:
                result_list.append(sentence)
                break
    return result_list

def mapVerbEntity(split_result,entity_list):
    result_list = []
    for sentence in split_result:
        index = -1
        dict_list = []
        for word in sentence :
            dic = dict()
            index = index+1
            if word[1] =='v' and len(word[0])>1:
                dic[word[0]+"_"+word[1]] =index
                dict_list.append(dic)
            else:
                for entity in entity_list:
                    if word[0] == entity[0]:
                        dic[word[0]+"_"+word[1]] = index
                        dict_list.append(dic)
                        break
        result_list.append(dict_list)
    return result_list


if __name__=="__main__":
    #读取文件
    thu1 = thulac.thulac()  #默认模式
    path = r"D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel"
    file_list = os.listdir(path) 
    for file_name in file_list:
        print(file_name)
        f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\'+file_name
                 ,'r',encoding = 'utf-8')
        file = f.read()
    #    print(file)
        json_file = json.loads(file)#转化为json格式
        text = json_file.get("text")#读取text
        
#        print(text)
        sentence_list = splitSentence(text)#将text分为句子列表
        location = file_name.find("_")
        jingdian_name = file_name[location+1:]
        keyWords = []
        splitKeyWords = thu1.cut(jingdian_name)
        for splitKeyWord in splitKeyWords:
            keyWords.append(splitKeyWord[0])
        keySentence = getKeySentence(sentence_list,keyWords)
        split_result = splitWord(keySentence,thu1)#使用thulac进行分词
        entity = json_file.get("bdlink_entity")#读取bdlink_entity的数据
        verbEntity = mapVerbEntity(split_result,entity)
        with open('D:\\python-file\\北京市旅游知识图谱\\verb-entity\\verb_entity_result\\'+file_name, 'w',encoding='utf-8') as json_file:
            for line in verbEntity:
                if len(line)!=0:
                    json_file.write(str(line)+'\n')
        
        f.close()