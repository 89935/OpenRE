# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:34:51 2019

@author: thinkpad
修改内容：用LTP对单个词进行词性标注
再用LTP对整句话先分词，再进行词性标注，不再去除停用词
加入时间名词，加入额外补充实体，考虑使用jieba分词，不考虑去除停用词
"""
import json
import re
import thulac
import os
import jieba
from entity_verb.nlp import NLP
from pyltp import Segmentor,SentenceSplitter,Postagger,NamedEntityRecognizer,Parser


class entity_verb_new:

    def __init__(self):
        """
        xlore识别出来的实体
        """
        f = open('..\\entity_verb_result\\' + "all_entity.json"
                 , 'r', encoding='utf-8')
        file = f.read()
        self.all_entity = json.loads(file)['all_entity']


        f.close()
        """
        时间名词
        """
        f = open('..\\entity_verb_result\\' + "时间名词.json"
                 , 'r', encoding='utf-8')
        file = f.read()
        self.tempNoun = json.loads(file)
        for noun in self.tempNoun:
            self.all_entity.append(noun)

        """
        LTP的NER额外补充名词
        """
        f = open('sentence_level2_result\\' + "jieba+LTP额外补充的命名实体长度大于1.json", 'r', encoding='utf-8')
        file = f.read()
        f.close()
        additional_entity_postag = json.loads(file)
        self.personList = []
        self.locationList = []
        self.organizationList = []
        for entity_postag in additional_entity_postag:
            entity = entity_postag.split('---')[0]
            self.all_entity.append(entity)
            postag = entity_postag.split('---')[1]
            if postag == 'ni':
                self.organizationList.append(entity)
            elif postag == 'nh':
                self.personList.append(entity)
            elif postag == 'ns':
                self.locationList.append(entity)

        for entity in self.all_entity:
            jieba.add_word(entity)
        print(self.all_entity)
    def not_empty(self,s):
        return s and "".join(s.split())


    def splitSentence(self,text):
        pattern = r'。|！|？|；|='
        result_list = re.split(pattern, text)
        result_list = list(filter(self.not_empty, result_list))
        #    print(result_list)
        return result_list


    def stopwordsList(self):
        """
        return:停用词列表
        """
        stop_list_Path = 'D:\python-file\\北京市旅游知识图谱\\verb-entity\\中文停用词.txt'
        f = open(stop_list_Path, 'r', encoding='utf-8')
        stopwords = [line.strip() for line in f.readlines()]
        #    print(stopwords)
        return stopwords


    def splitWord(self,sentence_list, thu1):
        result_list = []
        stopwords = self.stopwordsList()

        for sentence in sentence_list:
            sentence = sentence.strip()
            result_words = []
            words = thu1.cut(sentence)  # 进行一句话分词
            for word in words:
                if word[0] not in stopwords and len(word[0].strip()) != 0:
                    result_words.append(word)
            result_list.append(result_words)
        #    print(result_list)
        return result_list

    def splitWordOneSentence(self,sentence, thu1):
        stopwords = self.stopwordsList()

        sentence = sentence.strip()
        result_words = []
        words = thu1.cut(sentence)  # 进行一句话分词
        for word in words:
            if word[0] not in stopwords and len(word[0].strip()) != 0:
                result_words.append(word)
        return result_words

    def getKeySentence(sentence_list, keyWords):
        result_list = []
        for sentence in sentence_list:
            for keyWord in keyWords:
                if keyWord in sentence:
                    result_list.append(sentence)
                    break
        return result_list


    def mapVerbEntity(split_result, entity_list):
        result_list = []
        for sentence in split_result:
            index = -1
            dict_list = []
            for word in sentence:
                dic = dict()
                index = index + 1
                if word[1] == 'v' and len(word[0]) > 1:
                    dic[word[0] + "_" + word[1]] = index
                    dict_list.append(dic)
                else:
                    for entity in entity_list:
                        if word[0] == entity[0]:
                            dic[word[0] + "_" + word[1]] = index
                            dict_list.append(dic)
                            break
            result_list.append(dict_list)
        return result_list


    def mapEntity(self,sentence_list, all_entity,thu1,nlp,segmentor,postagger):
        stopwords = self.stopwordsList()
        entity_in_all_sentence =[]
        for sentence in sentence_list:
            # entity_in_each_sentence =[]

            flag = False
            entity_verb_dict = {}
            for entity in all_entity:
                # if entity in sentence:
                if sentence.find(entity)!=-1:
                    flag = True
                    location = 0
                    index = 0
                    while location<len(sentence):
                        location = sentence.find(entity,location)
                        if location ==-1:
                            break
                        else:
                            index +=1
                            if entity in self.tempNoun:
                                entity_verb_dict[str(index) + '#' + entity + '_AtempNoun' ] = location
                            elif entity in self.personList:
                                entity_verb_dict[str(index) + '#' + entity + '_Anh' ] = location
                            elif entity in self.locationList:
                                entity_verb_dict[str(index) + '#' + entity + '_Ans' ] = location
                            elif entity in self.organizationList:
                                entity_verb_dict[str(index) + '#' + entity + '_Ani' ] = location
                            else:
                                entity_verb_dict[str(index)+'#'+entity + '_' + nlp.get_postag(entity)] = location
                            location+=len(entity)
                    # entity_in_each_sentence.append(entity+'_'+str(sentence.find(entity)))

            if flag:
                # splitWordList = segmentor.segment(sentence)
                # result_words = []
                # for word in splitWordList:
                #     result_words.append(word)
                result_words = jieba.lcut(sentence)
                print(result_words)
                wordPosList = postagger.postag(result_words)
                result_pos = []
                for pos in wordPosList:
                    result_pos.append(pos)
                print(result_pos)
                # splitWordList = self.splitWordOneSentence(sentence,thu1)
                count = 0
                for index in range(len(result_words)):
                    word = result_words[index]
                    pos = result_pos[index]
                    # if word not in stopwords and pos== 'v':  # 如果该单词不在停用词表中，且为动词
                    if pos == 'v':  # 不去除停用词，只要是动词即可
                        entity_verb_dict[word+'_v_'+str(count)] = count  # 由于一句话中可能会出现多次，所以我们使用count来表明，该动词所在的位置。
                        # 而且一个动词也可能在一句话中出现多次，所以我们给动词+count，使动词唯一。
                    count += len(word)
            entity_verb_dict = sorted(entity_verb_dict.items(), key=lambda item: item[1])
            print(entity_verb_dict)
            entity_in_all_sentence.append(entity_verb_dict)
        return entity_in_all_sentence

    def readAllEntity(self,file = 'entity_verb_result\\' + "all_entity.json"):
        f = open(file
                 , 'r', encoding='utf-8')
        file = f.read()
        all_entity = json.loads(file)['all_entity']
        return all_entity


if __name__ == "__main__":
    # 读取文件
    entity_verb_new = entity_verb_new()
    """
    加载LTP的分词器和词性标注器
    """
    default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\'  # LTP模型文件目录
    segmentor = Segmentor()
    user_dict = "source\\user.txt"
    segmentor_flag = segmentor.load_with_lexicon(os.path.join(default_model_dir, 'cws.model'), user_dict)

    postagger = Postagger()
    postag_flag = postagger.load(os.path.join(default_model_dir, 'pos.model'))

    nlp = NLP()
    thu1 = thulac.thulac()  # 默认模式
    path = r"D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel"
    file_list = os.listdir(path)

    for file_name in file_list:
        print(file_name)
        f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\' + file_name
                 , 'r', encoding='utf-8')
        file = f.read()
        #    print(file)
        json_file = json.loads(file)  # 转化为json格式
        text = json_file.get("text")  # 读取text

        #        print(text)
        sentence_list = entity_verb_new.splitSentence(text)  # 将text分为句子列表
        noBlankSentenceList = []
        for sentence in sentence_list:
            sentence = sentence.replace(" ","")
            sentence = sentence.replace('\xa0',"")
            sentence = sentence.replace('\u3000',"")
            noBlankSentenceList.append(sentence)
        Entity_in_sentence = entity_verb_new.mapEntity(noBlankSentenceList, entity_verb_new.all_entity,thu1,nlp,segmentor,postagger)
        print(Entity_in_sentence)
        with open('sentence_level2_result\\V0.3\\' + file_name[:-3]+"json", 'w',
                  encoding='utf-8') as json_file:
            i = -1
            for line in Entity_in_sentence:
                i +=1
                sentence = noBlankSentenceList[i]
                line_dict = dict()
                if len(line) != 0:
                    line_dict[sentence] = line
                    json_file.write(json.dumps(line_dict,ensure_ascii=False) + '\n')



        # with open('entity_verb_result\\' + file_name, 'w',
        #           encoding='utf-8') as json_file:
        #     for line in Entity_in_sentence:
        #         if len(line) != 0:
        #             json_file.write(str(line) + '\n')

        f.close()