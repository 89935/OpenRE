# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:31:50 2020

@author: thinkpad
"""

# import pynlpir
from ctypes import c_char_p
import jieba
from pyltp import SentenceSplitter,Postagger,NamedEntityRecognizer,Parser
import os
from entity_verb.entity_verb_new import entity_verb_new
import thulac
import sys
sys.path.append("..") #跳出当前目录
from LTPNLP.bean.word_unit import WordUnit
from LTPNLP.bean.sentence_unit import SentenceUnit
from LTPNLP.core.entity_combine import EntityCombine

class NLP:
    """进行自然语言处理，包括分词，词性标注，命名实体识别，依存句法分析
    Attributes：
        default_user_dict_dir:str，用户自定义词典目录
        default_model_dir：str，ltp模型文件目录
    """

    entity_verb_new = entity_verb_new()
    all_entity = entity_verb_new.readAllEntity("../../entity_verb//entity_verb_result\\all_entity.json")
    default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\' #LTP模型文件目录
    
    def __init__(self,model_dir = default_model_dir,all_entity= all_entity ):
        self.default_model_dir = model_dir
        #初始化分词器
        #使用jieba分析，将抽取出的所有实体，作为词典加入jieba中
        for entity in all_entity:
            jieba.add_word(entity,100000)
        jieba.add_word("天府永藏展",100000)
        # jieba.add_word("始建于",100000)
        # pynlpir.open()#初始化分词器
        # #添加用户词典（法律文书大辞典与清华大学法律词典），这种方式是添加进内存中，速度更快
        # files = os.listdir(user_dict_dir)
        # for file in files:
        #     file_path = os.path.join(user_dict_dir,file)
        #     #文件夹则跳过
        #     if os.path.isdir(file):
        #         continue
        #     with open(file_path,'r',encoding = 'utf-8') as f:
        #         line = f.readline()
        #         while line:
        #             word = line.strip('\n').strip()
        #             pynlpir.nlpir.AddUserWord(c_char_p(word.encode()))
        #             line = f.readline()
        #加载ltp模型
        #词性标注模型
        self.postagger = Postagger()
        postag_flag = self.postagger.load(os.path.join(self.default_model_dir,'pos.model'))
        #命名实体识别模型
        self.recognizer = NamedEntityRecognizer()
        ner_flag = self.recognizer.load(os.path.join(self.default_model_dir,'ner.model'))
        #依存句法分析模型
        self.parser = Parser()
        parser_flag = self.parser.load(os.path.join(self.default_model_dir,'parser.model'))
        
        if postag_flag or ner_flag or parser_flag:#可能有错误
            print('load model failed')
        
    def segment(self,sentence,entity_postag = dict()):
        """
        采用NLPIR进行分词处理
        Args:
            Sentence:String，句子
            entity_postag : dict，实体词性词典，默认为空集合，分析每一个案例的结构化文本时产生
        Returns:
            lemma:list，分词结果
        """
        #添加实体词典
        # if entity_postag:
        #     for entity in entity_postag:
        #         pynlpir.nlpir.AddUserWord(c_char_p(entity.encode()))
        # pynlpir.nlpir.AddUserWord(c_char_p('前任'.encode()))#单个用户加入示例
        # pynlpir.nlpir.AddUserWord(c_char_p('习近平'.encode()))#单个用户加入示例
        #分词，不进行词性标注
        result = jieba.cut(sentence)
        # pynlpir.close()  # 释放
        lemmas = []
        for lemma in result:
            lemmas.append(lemma)
        # lemmas = pynlpir.segment(sentence,pos_tagging=False)
        #pynlpir.close() #释放
        return lemmas
    
    def getPostag(self):
        return self.postagger    
    
    def postag(self,lemmas):
        """
        Parameters
        ----------
        lemmas : List，分词后的结果
        entity_dict：Set，实体词典，处理具体的一则判决书的结构化文本时产生
        Returns
        -------
        words:WordUnit List，包括分词与词性标注的结果
        """
        words= []
        #词性标注
        postags = self.postagger.postag(lemmas)
        for i in range(len(lemmas)):
            #存储分词与词性标记后的词单元WordUnit，编号从1开始
            word = WordUnit(i+1,lemmas[i],postags[i])
            words.append(word)
        #self.postagger.release() #释放
        return words
    
    def get_postag(self,word):
        """获得单个词的词性标注
        Args:
            word:str,单词
        Returns:
            pos_tag:str，该单词的词性标注
        """
        pos_tag = self.postagger.postag([word])
        return pos_tag[0]
    
    def netag(self,words):
        """
        命名实体识别，并对分词与词性标注后的结果进行命名实体识别与合并
        Parameters
            words : WordUnit list，包括分词与词性标注结果
        Returns
            words_netag：WordUnit list，包含分词，词性标注与命名实体识别的结果
        """
        lemmas = []#存储分词后的结果
        postags=[] #存储词性标注结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        #命名实体识别
        netags = self.recognizer.recognize(lemmas,postags)
        words_netag = EntityCombine().combine(words,netags)
        return words_netag
    
    def parse(self,words):
        """
        对分词，词性标注与命名实体识别后的结果进行依存句法分析（命名实体识别可选）
        Args:
            words_netag：WordUnit list，包含分词，词性标注与命名实体识别结果
        Returns
            *：sentenceUnit 句子单元
        """
        lemmas = [] #分词结果
        postags = [] #词性标注结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        #依存句法分析
        arcs = self.parser.parse(lemmas,postags)
        for i in range(len(arcs)):
            words[i].head = arcs[i].head
            words[i].dependency  = arcs[i].relation
        return SentenceUnit(words)
    
    def close(self):
        """
        关闭与释放
        """
        # pynlpir.close()
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()

    def getSPO1(self,sentence_list):
        for sentence in sentence_list:
            lemmas = nlp.segment(sentence)

            print(lemmas)

            # 词性标注测试
            print('***' + '词性标注测试' + '***')
            words = nlp.postag(lemmas)
            # for word in words:
            #     print(word.to_string())
            # print(words)

            # 命名实体识别与合并测试
            print('***' + '命名实体识别与合并测试' + '***')
            words_netag = nlp.netag(words)
            # for word in words_netag:
            #     print(word.to_string())

            # 依存句法分析测试
            print('***' + '依存句法分析测试' + '***')
            sentence = nlp.parse(words_netag)
            print(sentence.to_string())

            verb = True
            # entity = "乾清宫"
            for item in sentence.words:
                if (item.head_word == None and item.lemma == verb ) or (item.lemma == verb and
                                                                      item.dependency == "COO" and item.head_word.head_word == None):
                    relation_verb = item
                    if item.head_word==None:
                        verbId = item.ID
                    elif item.head_word.head_word == None:
                        verbId = item.ID
                        verbId2 = item.head_word.ID
                    O_dict = dict()
                    S_dict = dict()
                    OBJ = None
                    SUB = None
                    for item in sentence.words:
                        if item.dependency == "SBV" and item.head_word.ID == verbId:
                            # if SUB == None or SUB.lemma != entity:
                            SUB = item
                            S_dict[SUB.lemma] = SUB.ID
                        if item.dependency == "VOB" and item.head_word.ID == verbId:
                            OBJ = item
                            O_dict[OBJ.lemma] = OBJ.ID
                    if SUB == None:
                        for item in sentence.words:
                            if item.dependency == "SBV" and item.head_word.ID == verbId2:
                                # if SUB == None or SUB.lemma != entity:
                                SUB = item
                                S_dict[SUB.lemma] = SUB.ID
                    if OBJ == None:
                        for item in sentence.words:
                            if item.dependency == "VOB" and item.head_word.ID == verbId2:
                                OBJ = item
                                O_dict[OBJ.lemma] = OBJ.ID

                    OBJList = []
                    flag = True
                    while flag == True:
                        len1 = len(S_dict)
                        len2 = len(O_dict)
                        for item in sentence.words:
                            if SUB !=None and item.head_word!=None:
                                SUBList = S_dict.values()
                                if item.head_word.ID in SUBList and (item.dependency =="ATT"
                                        or item.dependency == "COO"):
                                    SUBATT = item
                                    S_dict[SUBATT.lemma] = SUBATT.ID
                            if OBJ != None and item.head_word != None:
                                OBJList = O_dict.values()
                                if item.head_word.ID in  OBJList and (item.dependency == "ATT" )  :
                                    OBJATT = item
                                    O_dict[OBJATT.lemma] = OBJATT.ID
                            if len(S_dict)!=len1 or len(O_dict)!=len2:
                                flag = True
                            else:
                                flag = False
                    O_dict = sorted(O_dict.items(), key=lambda item: item[1])
                    S_dict = sorted(S_dict.items(), key=lambda item: item[1])
                    Object = ""
                    Subject = ""
                    for i in O_dict:
                        Object += i[0]
                    for i in S_dict:
                        Subject += i[0]
                    if SUB != None:
                        print((Subject, verb, Object))

                    S_dict2 = dict()
                    O_dict2 = dict()
                    SUB_COO = None
                    OBJ_COO = None
                    for item in sentence.words:
                        if item.head_word != None:
                            if SUB != None and item.dependency == "COO" and item.head_word.ID == SUB.ID:
                                # if SUB == None or SUB.lemma != entity:
                                SUB_COO = item
                                S_dict2[SUB_COO.lemma] = SUB_COO.ID
                        if item.head_word != None:
                            if item.dependency == "COO" and item.head_word.ID == OBJ.ID:
                                OBJ_COO = item
                                O_dict2[OBJ_COO.lemma] = OBJ_COO.ID

                    flag = True
                    while flag == True:
                        len1 = len(S_dict2)
                        len2 = len(O_dict2)
                        for item in sentence.words:
                            if SUB_COO != None and item.head_word != None:
                                SUBList = S_dict2.values()
                                if item.head_word.ID in SUBList and item.dependency == "ATT":
                                    SUBATT = item
                                    S_dict2[SUBATT.lemma] = SUBATT.ID
                            if OBJ_COO != None and item.head_word != None:
                                OBJList = O_dict2.values()
                                if item.head_word.ID in OBJList and item.dependency == "ATT":
                                    OBJATT = item
                                    O_dict2[OBJATT.lemma] = OBJATT.ID
                            if len(S_dict2) != len1 or len(O_dict2) != len2:
                                flag = True
                            else:
                                flag = False
                    O_dict2 = sorted(O_dict2.items(), key=lambda item: item[1])
                    S_dict2 = sorted(S_dict2.items(), key=lambda item: item[1])
                    if len(O_dict2) or len(S_dict2):
                        if len(O_dict2) == 0:
                            O_dict2 = O_dict
                        if len(S_dict2) == 0:
                            S_dict2 = S_dict

                        Object = ""
                        Subject = ""
                        for i in O_dict2:
                            Object += i[0]
                        for i in S_dict2:
                            Subject += i[0]
                        if SUB != None:
                            print((Subject, verb, Object))
    def getSPO2(self,sentence_list):
        for sentence in sentence_list:
            lemmas = nlp.segment(sentence)

            print(lemmas)

            # 词性标注测试
            print('***' + '词性标注测试' + '***')
            words = self.postag(lemmas)
            # for word in words:
            #     print(word.to_string())
            # print(words)

            # 命名实体识别与合并测试
            print('***' + '命名实体识别与合并测试' + '***')
            words_netag = nlp.netag(words)
            # for word in words_netag:
            #     print(word.to_string())

            # 依存句法分析测试
            print('***' + '依存句法分析测试' + '***')
            sentence = nlp.parse(words_netag)
            print(sentence.to_string())

            # verb = True
            # entity = "乾清宫"
            for item in sentence.words:
                if (item.head_word == None and item.postag == "v" ) or (item.postag == "v" and
                                                                      item.dependency == "COO" and item.head_word.head_word == None):
                    relation_verb = item
                    if item.head_word==None:
                        verbId = item.ID
                    elif item.head_word.head_word == None:
                        verbId = item.ID
                        verbId2 = item.head_word.ID
                    O_dict = dict()
                    S_dict = dict()
                    OBJ = None
                    SUB = None
                    for item in sentence.words:
                        if item.dependency == "SBV" and item.head_word.ID == verbId:
                            # if SUB == None or SUB.lemma != entity:
                            SUB = item
                            S_dict[SUB.lemma] = SUB.ID
                        if (item.dependency == "VOB" and item.head_word.ID == verbId) or (item.dependency == "POB" and item.head_word.ID == verbId)\
                                or (item.dependency == "POB" and item.head_word.postag == "p" and item.head_word.dependency == "CMP"
                                    and item.head_word.head_word.ID
                        == verbId):
                            OBJ = item
                            O_dict[OBJ.lemma] = OBJ.ID
                    if SUB == None:
                        for item in sentence.words:
                            if item.dependency == "SBV" and item.head_word.ID == verbId2:
                                # if SUB == None or SUB.lemma != entity:
                                SUB = item
                                S_dict[SUB.lemma] = SUB.ID
                    if OBJ == None:
                        for item in sentence.words:
                            if item.dependency == "VOB" and item.head_word.ID == verbId2:
                                OBJ = item
                                O_dict[OBJ.lemma] = OBJ.ID

                    OBJList = []
                    flag = True
                    while flag == True:
                        len1 = len(S_dict)
                        len2 = len(O_dict)
                        for item in sentence.words:
                            if SUB !=None and item.head_word!=None:
                                SUBList = S_dict.values()
                                if item.head_word.ID in SUBList and (item.dependency =="ATT"
                                        or item.dependency == "COO"):
                                    SUBATT = item
                                    S_dict[SUBATT.lemma] = SUBATT.ID
                            if OBJ != None and item.head_word != None:
                                OBJList = O_dict.values()
                                if item.head_word.ID in  OBJList and (item.dependency == "ATT" )  :
                                    OBJATT = item
                                    O_dict[OBJATT.lemma] = OBJATT.ID
                            if len(S_dict)!=len1 or len(O_dict)!=len2:
                                flag = True
                            else:
                                flag = False
                    O_dict = sorted(O_dict.items(), key=lambda item: item[1])
                    S_dict = sorted(S_dict.items(), key=lambda item: item[1])
                    Object = ""
                    Subject = ""
                    for i in O_dict:
                        Object += i[0]
                    for i in S_dict:
                        Subject += i[0]
                    if SUB != None:
                        print((Subject, relation_verb.lemma, Object))

                    S_dict2 = dict()
                    O_dict2 = dict()
                    SUB_COO = None
                    OBJ_COO = None
                    for item in sentence.words:
                        if item.head_word != None:
                            if SUB != None and item.dependency == "COO" and item.head_word.ID == SUB.ID:
                                # if SUB == None or SUB.lemma != entity:
                                SUB_COO = item
                                S_dict2[SUB_COO.lemma] = SUB_COO.ID
                        if item.head_word != None and OBJ!=None:
                            if item.dependency == "COO" and item.head_word.ID == OBJ.ID:
                                OBJ_COO = item
                                O_dict2[OBJ_COO.lemma] = OBJ_COO.ID

                    flag = True
                    while flag == True:
                        len1 = len(S_dict2)
                        len2 = len(O_dict2)
                        for item in sentence.words:
                            if SUB_COO != None and item.head_word != None:
                                SUBList = S_dict2.values()
                                if item.head_word.ID in SUBList and item.dependency == "ATT":
                                    SUBATT = item
                                    S_dict2[SUBATT.lemma] = SUBATT.ID
                            if OBJ_COO != None and item.head_word != None:
                                OBJList = O_dict2.values()
                                if item.head_word.ID in OBJList and item.dependency == "ATT":
                                    OBJATT = item
                                    O_dict2[OBJATT.lemma] = OBJATT.ID
                            if len(S_dict2) != len1 or len(O_dict2) != len2:
                                flag = True
                            else:
                                flag = False
                    O_dict2 = sorted(O_dict2.items(), key=lambda item: item[1])
                    S_dict2 = sorted(S_dict2.items(), key=lambda item: item[1])
                    if len(O_dict2) or len(S_dict2):
                        if len(O_dict2) == 0:
                            O_dict2 = O_dict
                        if len(S_dict2) == 0:
                            S_dict2 = S_dict

                        Object = ""
                        Subject = ""
                        for i in O_dict2:
                            Object += i[0]
                        for i in S_dict2:
                            Subject += i[0]
                        if SUB != None:
                            print((Subject, relation_verb.lemma, Object))

    def getSPO(self,sentence_list):
        for sentence in sentence_list:
            print(sentence)
            lemmas = self.segment(sentence)

            # print(lemmas)

            # 词性标注测试
            # print('***' + '词性标注测试' + '***')
            words = self.postag(lemmas)
            # for word in words:
            #     print(word.to_string())
            # print(words)

            # 命名实体识别与合并测试
            # print('***' + '命名实体识别与合并测试' + '***')
            words_netag = self.netag(words)
            # for word in words_netag:
            #     print(word.to_string())

            # 依存句法分析测试
            # print('***' + '依存句法分析测试' + '***')
            sentence = self.parse(words_netag)
            # print(sentence.to_string())

            # verb = True
            # entity = "乾清宫"
            for item in sentence.words:
                if (item.head_word == None and item.postag == "v" ) or (item.postag == "v" and
                                                                      item.dependency == "COO" and item.head_word.head_word == None):
                    relation_verb = item
                    if item.head_word==None:
                        verbId = item.ID
                        verbId2 = None
                    elif item.head_word.head_word == None:
                        verbId = item.ID
                        verbId2 = item.head_word.ID
                    O_dict = dict()
                    S_dict = dict()
                    OBJ = None
                    SUB = None
                    for item in sentence.words:
                        if item.dependency == "SBV" and item.head_word.ID == verbId:
                            # if SUB == None or SUB.lemma != entity:
                            SUB = item
                            S_dict[SUB.ID] = SUB.lemma
                        if (item.dependency == "VOB" and item.head_word.ID == verbId) or (item.dependency == "POB" and item.head_word.ID == verbId)\
                                or (item.dependency == "POB" and item.head_word.postag == "p" and item.head_word.dependency == "CMP"
                                    and item.head_word.head_word.ID== verbId):
                            OBJ = item
                            O_dict[OBJ.ID] = OBJ.lemma
                            # if item.dependency == "POB" and item.head_word.postag == "p" and item.head_word.dependency == "CMP" \
                            #             and item.head_word.head_word.ID == verbId:
                            #     verb_p = item.head_word
                            # O_dict[OBJ.lemma] = OBJ.ID
                    if SUB == None:
                        for item in sentence.words:
                            if item.dependency == "SBV" and item.head_word.ID == verbId2:
                                # if SUB == None or SUB.lemma != entity:
                                SUB = item
                                S_dict[SUB.ID] = SUB.lemma
                    if OBJ == None:
                        for item in sentence.words:
                            if item.dependency == "VOB" and item.head_word.ID == verbId2:
                                OBJ = item
                                O_dict[OBJ.ID] = OBJ.lemma

                    OBJList = []
                    flag = True
                    while flag == True:
                        len1 = len(S_dict)
                        len2 = len(O_dict)
                        for item in sentence.words:
                            if SUB !=None and item.head_word!=None:
                                SUBList = S_dict.keys()
                                if item.head_word.ID in SUBList and (item.dependency =="ATT"
                                        or item.dependency == "COO"):
                                    SUBATT = item
                                    S_dict[SUBATT.ID] = SUBATT.lemma
                            if OBJ != None and item.head_word != None:
                                OBJList = O_dict.keys()
                                if item.head_word.ID in  OBJList and (item.dependency == "ATT" or item.dependency == "COO")  :
                                    OBJATT = item
                                    # if item.dependency!="COO":
                                    O_dict[OBJATT.ID] = OBJATT.lemma
                                    # else:
                                    #     O_dict[OBJATT.ID] = OBJATT.lemma+" "

                            if len(S_dict)!=len1 or len(O_dict)!=len2:
                                flag = True
                            else:
                                flag = False
                    O_dict = sorted(O_dict.items(), key=lambda item: item[0])
                    S_dict = sorted(S_dict.items(), key=lambda item: item[0])
                    Object = ""
                    Subject = ""
                    for i in O_dict:
                        Object += i[1]
                    for i in S_dict:
                        Subject += i[1]
                    if SUB != None:
                        print((Subject, relation_verb.lemma, Object))

                    S_dict2 = dict()
                    O_dict2 = dict()
                    SUB_COO = None
                    OBJ_COO = None
                    for item in sentence.words:
                        if item.head_word != None:
                            if SUB != None and item.dependency == "COO" and item.head_word.ID == SUB.ID:
                                # if SUB == None or SUB.lemma != entity:
                                SUB_COO = item
                                S_dict2[SUB_COO.ID] = SUB_COO.lemma
                        if item.head_word != None and OBJ!=None:
                            if item.dependency == "COO" and item.head_word.ID == OBJ.ID:
                                OBJ_COO = item
                                O_dict2[OBJ_COO.ID] = OBJ_COO.lemma

                    flag = True
                    while flag == True:
                        len1 = len(S_dict2)
                        len2 = len(O_dict2)
                        for item in sentence.words:
                            if SUB_COO != None and item.head_word != None:
                                SUBList = S_dict2.keys()
                                if item.head_word.ID in SUBList and item.dependency == "ATT":
                                    SUBATT = item
                                    S_dict2[SUBATT.ID] = SUBATT.lemma
                            if OBJ_COO != None and item.head_word != None:
                                OBJList = O_dict2.keys()
                                if item.head_word.ID in OBJList and item.dependency == "ATT":
                                    OBJATT = item
                                    O_dict2[OBJATT.ID] = OBJATT.lemma
                            if len(S_dict2) != len1 or len(O_dict2) != len2:
                                flag = True
                            else:
                                flag = False
                    O_dict2 = sorted(O_dict2.items(), key=lambda item: item[0])
                    S_dict2 = sorted(S_dict2.items(), key=lambda item: item[0])
                    if len(O_dict2) or len(S_dict2):
                        if len(O_dict2) == 0:
                            O_dict2 = O_dict
                        if len(S_dict2) == 0:
                            S_dict2 = S_dict

                        Object = ""
                        Subject = ""
                        for i in O_dict2:
                            Object += i[1]
                        for i in S_dict2:
                            Subject += i[1]
                        if SUB != None :
                            print((Subject, relation_verb.lemma, Object))


if __name__ == '__main__':
    nlp = NLP()
    #分词测试
    print('***'+'分词测试'+'***')
    # sentence = u'交泰殿：位于乾清宫以北'
    # sentence = u'乾清宫：内廷中心建筑，位于乾清门以北'
    sentence_list = [
#         "北京故宫博物院建立于1925年10月10日，位于北京故宫紫禁城内",
# "故宫为中国明、清两代（公元1368～1911年）的皇宫，依照中国古代星象学说，紫微垣（即北极星）位于中天，乃天帝所居，天人对应，是以故宫又称紫禁城",
# "北京故宫博物院位于北京城中心，东西宽753米，南北长961米，占地面积723600余平方米，周围环以10米高的城墙和52米宽的护城河（筒子河）",
# "明代嘉靖年建，位于内廷乾清宫西侧",
# "武英殿始建于明初，位于外朝熙和门以西",
# "位于太和门广场，共5座，单孔拱券式",
# "太和殿：外朝中心建筑，位于太和门以北",
# "中和殿：位于太和殿以北",
# "保和殿：位于中和殿以北",
# "乾清宫：内廷中心建筑，位于乾清门以北",
# "交泰殿：位于乾清宫以北",
# "坤宁宫：位于交泰殿以北",
# "养心殿是清雍正以后的皇帝寝宫，位于内廷西六宫区以南、后三宫区以西",
"皇极殿：紫禁城东北部宁寿宫区的中心建筑，位于宁寿宫区内，仅在：元旦、清明、五一、端午小长假各开放5天（从政府公布休假日期的前一天开始开放）",
# "设在外朝武英殿区，位于太和门广场以西",
# "设在外朝文华殿区，位于太和门广场以东",
# "设在奉先殿区，位于内廷东六宫区以南、宁寿宫区以",
# "宁寿宫区位于宫城东北部，是乾隆时期修建的太上皇宫殿区，包含九龙壁、皇极殿、乾隆花园、珍妃井等著名景点",
"珍宝馆、石鼓馆和戏曲馆这三个常设展馆位于宁寿宫区内",
# "天府永藏展：设在保和殿西庑房及西北崇楼，位于外朝前三殿区西侧，展示历代皇家收藏传统与清宫收藏类别",
# "清宫卤簿仪仗展：设在太和门西庑房，位于太和门广场西侧，展示清宫卤簿和仪仗用具",
# "斋宫：位于内廷后三宫区以东、东六宫区以南"

                     ]
    # sentence = u'明代嘉靖年建，位于内廷乾清宫西侧'
    nlp.getSPO(sentence_list)
    nlp.close()



            # if item.ID != sentence.words[0].head_word.ID:
            #     print(item.head_word.ID)
            # else:
            #     print(0)
        # sob = sentence.words[]