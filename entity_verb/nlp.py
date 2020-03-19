# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:31:50 2020

@author: thinkpad
"""

import json

from ctypes import c_char_p
import jieba
from pyltp import SentenceSplitter,Segmentor,Postagger,NamedEntityRecognizer,Parser
import os
import thulac

class NLP:
    default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\' #LTP模型文件目录
    
    def __init__(self,model_dir = default_model_dir):
        self.default_model_dir = model_dir

        #词性标注模型
        self.postagger = Postagger()
        postag_flag = self.postagger.load(os.path.join(self.default_model_dir,'pos.model'))

    def get_postag(self,word):
        """获得单个词的词性标注
        Args:
            word:str,单词
        Returns:
            pos_tag:str，该单词的词性标注
        """
        pos_tag = self.postagger.postag([word, ])
        return pos_tag[0]

    def close(self):
        """
        关闭与释放
        """
        self.postagger.release()

if __name__ == '__main__':

    nlp = NLP()
    # print(nlp.get_postag("收藏"))
    default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\'  # LTP模型文件目录
    segmentor = Segmentor()
    user_dict = "source\\user.txt"
    segmentor_flag = segmentor.load_with_lexicon(os.path.join(default_model_dir, 'cws.model'), user_dict)

    postagger = Postagger()
    postag_flag = postagger.load(os.path.join(default_model_dir, 'pos.model'))
    # f = open("entity_verb_result\\verb_frequence_len2_v2.json", "r", encoding="utf-8")
    # file = f.read()
    # json_file = json.loads(file)
    # all_word = json_file.keys()
    # f.close()
    # # print(all_word)
    # # print(len(all_word))
    # thu1 = thulac.thulac()
    # print("ltp的分词结果:")
    words = segmentor.segment("圜丘坛之北是皇穹宇")
    resultWords = []
    for word in words:
        resultWords.append(word)
    print(resultWords)
    print("ltp的词性标注结果:")
    poss = postagger.postag(resultWords)
    resultPos = []
    for pos in poss:
        resultPos.append(pos)
    print(resultPos)
    #
    # poss = postagger.postag(words)
    # resultPos = []
    # for pos in poss:
    #     resultPos.append(pos)
    # print(resultPos)
    # print("ltp结果postagger.postag([\"奕訢\"])[0]:"+postagger.postag(["奕訢"])[0])
    # print("thulac的结果：")
    # print(thu1.cut("1851年，恭亲王奕訢成为宅子的主人，恭王府的名称也因此得来。"))
    # print(thu1.cut("奕訢"))





    # count = 0
    # for word in all_word:
    #     if  len(thu1.cut(word)) ==1 and thu1.cut(word)[0][1] != 'v':
    #         print("\""+word+"\""  + '的词性：' + thu1.cut(word)[0][1])
    #         count+=1
    #     elif len(thu1.cut(word))>1:
    #         flag = False
    #         for word_pos in thu1.cut(word):
    #             if word_pos[1] == 'v':
    #                 flag = True
    #         if flag==False:
    #             print("\""+word+"\"" + '的词性：' + thu1.cut(word)[0][1])
    #             count += 1
    # # word = "祈年殿"
    # print(count)

    
    