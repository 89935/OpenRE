# -*- coding: utf-8 -*-
# 初步实现，但未加DSFN的约束
# import pynlpir
from ctypes import c_char_p
import jieba
from pyltp import Segmentor, Postagger, NamedEntityRecognizer, Parser
import os
from entity_verb.entity_verb_new import entity_verb_new
import thulac
import sys
import numpy as np
sys.path.append("..")  # 跳出当前目录
from LTPNLP.bean.word_unit import WordUnit
from LTPNLP.bean.sentence_unit import SentenceUnit
from LTPNLP.core.entity_combine import EntityCombine
import json,re

class DSFN:
    """进行自然语言处理，包括分词，词性标注，命名实体识别，依存句法分析
    Attributes：
        default_user_dict_dir:str，用户自定义词典目录
        default_model_dir：str，ltp模型文件目录
    """

    entity_verb_new = entity_verb_new()
    all_entity = entity_verb_new.readAllEntity("../../entity_verb//entity_verb_result\\all_entity.json")
    default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\'  # LTP模型文件目录

    def __init__(self, model_dir=default_model_dir, all_entity=all_entity):
        self.default_model_dir = model_dir
        # 加载ltp模型
        #
        default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\'  # LTP模型文件目录
        self.segmentor = Segmentor()
        user_dict = "..\\source\\user.txt"
        segmentor_flag = self.segmentor.load_with_lexicon(os.path.join(default_model_dir, 'cws.model'), user_dict)
        # 词性标注模型
        self.postagger = Postagger()
        postag_flag = self.postagger.load(os.path.join(self.default_model_dir, 'pos.model'))
        # 命名实体识别模型
        self.recognizer = NamedEntityRecognizer()
        ner_flag = self.recognizer.load(os.path.join(self.default_model_dir, 'ner.model'))
        # 依存句法分析模型
        self.parser = Parser()
        parser_flag = self.parser.load(os.path.join(self.default_model_dir, 'parser.model'))

        if segmentor_flag or postag_flag or ner_flag or parser_flag:  # 可能有错误
            print('load model failed')

    def segment(self, sentence, entity_postag=dict()):
        words = self.segmentor.segment(sentence)
        lemmas = []
        for lemma in words:
            lemmas.append(lemma)
        return lemmas

    def getPostag(self):
        return self.postagger

    def postag(self, lemmas):
        """
        Parameters
        ----------
        lemmas : List，分词后的结果
        entity_dict：Set，实体词典，处理具体的一则判决书的结构化文本时产生
        Returns
        -------
        words:WordUnit List，包括分词与词性标注的结果
        """
        words = []
        # 词性标注
        postags = self.postagger.postag(lemmas)
        for i in range(len(lemmas)):
            # 存储分词与词性标记后的词单元WordUnit，编号从1开始
            word = WordUnit(i + 1, lemmas[i], postags[i])
            words.append(word)
        # self.postagger.release() #释放
        return words

    def get_postag(self, word):
        """获得单个词的词性标注
        Args:
            word:str,单词
        Returns:
            pos_tag:str，该单词的词性标注
        """
        pos_tag = self.postagger.postag([word])
        return pos_tag[0]

    def netag(self, words):
        """
        命名实体识别，并对分词与词性标注后的结果进行命名实体识别与合并
        Parameters
            words : WordUnit list，包括分词与词性标注结果
        Returns
            words_netag：WordUnit list，包含分词，词性标注与命名实体识别的结果
        """
        lemmas = []  # 存储分词后的结果
        postags = []  # 存储词性标注结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        # 命名实体识别
        netags = self.recognizer.recognize(lemmas, postags)
        words_netag = EntityCombine().combine(words, netags)
        return words_netag

    def parse(self, words):
        """
        对分词，词性标注与命名实体识别后的结果进行依存句法分析（命名实体识别可选）
        Args:
            words_netag：WordUnit list，包含分词，词性标注与命名实体识别结果
        Returns
            *：sentenceUnit 句子单元
        """
        lemmas = []  # 分词结果
        postags = []  # 词性标注结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        # 依存句法分析
        arcs = self.parser.parse(lemmas, postags)
        for i in range(len(arcs)):
            words[i].head = arcs[i].head
            words[i].dependency = arcs[i].relation
        return SentenceUnit(words)

    def close(self):
        """
        关闭与释放
        """
        # pynlpir.close()
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()

    def splitSentence(self,text):
        pattern = r'。|！|？|；|='
        result_list = re.split(pattern, text)
        result_list = list(filter(self.not_empty, result_list))
        #    print(result_list)
        return result_list

    def not_empty(self,s):
        return s and "".join(s.split())

    def dsfn1_2_3_4COO(self, sentence, item1, item2):
        allTripes = []

        """
        判断两个实体是否属于DSFN1的情况，并输出三元组
        """
        if (item1.dependency == "ATT"):
            AttWord = item1.head_word
            AttWordDict = dict()
            AttWordStr = ""
            while AttWord.ID < item2.ID:
                AttWordDict[AttWord.ID] = AttWord.lemma
                # AttWordStr += AttWord.lemma
                if (AttWord.dependency == "ATT"):
                    AttWord = AttWord.head_word
                else:
                    break

            if (AttWord.ID == item2.ID):
                flag = True
                while flag:
                    len1 = len(AttWordDict)
                    AttList = AttWordDict.keys()
                    for id in range(item1.ID + 1, item2.ID):
                        item = sentence.get_word_by_id(id)
                        if item.head_word != None and item.head_word.ID in AttList and (item.dependency == "ATT"):
                            AttWordDict[item.ID] = item.lemma
                    if len1 == len(AttWordDict):
                        flag = False
                    else:
                        flag = True
                AttWordDict = sorted(AttWordDict.items(), key=lambda item: item[0])
                AttWordStr = ""
                for i in AttWordDict:
                    AttWordStr += i[1]
                # print("三元组：（" + item1.lemma + "，" + AttWordStr + "，" + item2.lemma + "）")
                allTripes.append([item1.lemma, AttWordStr, item2.lemma])
        """
        判断两个实体是否属于DSFN1的情况，并输出三元组
        """

        """
        考虑DSFN2的情况
        """
        if item1.dependency == "SBV":
            pred1 = item1.head_word
            predDict = dict()
            predDict[pred1.ID] = pred1.lemma

            if item2.dependency == "VOB":
                pred2 = item2.head_word
                predDict[pred2.ID] = pred2.lemma
                if (len(predDict) == 1):
                    PredWordStr = ""
                    for i in predDict:
                        PredWordStr += predDict[i]
                    # print("DSFN2三元组：（" + item1.lemma + "，" + PredWordStr + "，" + item2.lemma + "）")
                    allTripes.append([item1.lemma, PredWordStr, item2.lemma])
                    """
                    新加，为了考虑“习近平视察和访问上海”的情况
                    """
                if len(predDict) ==2:
                    num = self.get_entity_num_between(pred1,pred2,sentence)
                    # print("pred1:"+pred1.lemma+",pred2:"+pred2.lemma+",num:"+str(num))
                    if num == 0:
                        # print("DSFN2三元组：（" + item1.lemma + "，" + pred1.lemma + "，" + item2.lemma + "）")
                        allTripes.append([item1.lemma, pred1.lemma, item2.lemma])
                        # print("DSFN2三元组：（" + item1.lemma + "，" + pred2.lemma + "，" + item2.lemma + "）")
                        allTripes.append([item1.lemma, pred2.lemma, item2.lemma])



        """
        DSFN3.0
        """
        pred = None
        if item1.dependency == "SBV" and item2.dependency == "POB":
            pred = item1.head_word
            prep = item2.head_word
        elif item1.dependency == "FOB" and item2.dependency == "POB":  # 考虑介词为“被”的情况，如 “小王被小明所陷害”
            pred = item1.head_word
            prep = item2.head_word
            c = item1
            item1 = item2
            item2 = c
        if pred != None and prep != None:
            if prep.dependency == "ADV":
                if prep.head_word.ID == pred.ID:
                    pred2 = None
                    object = None
                    objectForPred2 = None
                    for i in range(pred.ID + 1, len(sentence.words) + 1):
                        item = sentence.get_word_by_id(i)

                        if item.dependency == "VOB" and item.head_word.ID == pred.ID:
                            object = item
                            objectDict = dict()
                            objectDict[object.ID] = object
                            for word in sentence.words:
                                if word.head_word != None and word.dependency == "ATT" and word.head_word.ID == object.ID:
                                    objectDict[word.ID] = word
                            objectDict = sorted(objectDict.items(), key=lambda item: item[0])
                            objectStr = ""
                            for objectItem in objectDict:
                                objectStr += objectItem[1].lemma
                            # print(
                            #     "DSFN3三元组：（" + item1.lemma + "，" + pred.lemma + "" + objectStr + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred.lemma + "" + objectStr, item2.lemma])
                            # print("DSFN3三元组：（" + item1.lemma + "，" + pred.lemma + "" + object.lemma + "，" + item2.lemma + "）")
                            # allTripes.append([item1.lemma, pred.lemma + "" + object.lemma, item2.lemma])
                    if object == None:
                        # print("DSFN3三元组：（" + item1.lemma + "，" + pred.lemma + "，" + item2.lemma + "）")
                        allTripes.append([item1.lemma, pred.lemma , item2.lemma])
        """
        DSFN4
        """
        pred = None
        prep = None
        prep1 = None
        pred2 = None
        if item1.dependency == "SBV" and item2.dependency == "POB":
            pred = item1.head_word
            prep = item2.head_word
            if prep.dependency == "CMP":
                pred2 = prep.head_word
                if pred2.ID == pred.ID:
                    # print("DSFN4三元组：（" + item1.lemma + "，" + pred.lemma + "" + prep.lemma + "，" + item2.lemma + "）")
                    allTripes.append([item1.lemma, pred.lemma + "" + prep.lemma, item2.lemma])
                else :
                    num = self.get_entity_num_between(pred1, pred2, sentence)
                    # print("pred1:"+pred1.lemma+",pred2:"+pred2.lemma+",num:"+str(num))
                    if num == 0:
                        for word in sentence.words:
                            if word.dependency == "CMP" and word.head_word.ID == pred.ID:
                                prep1 = word
                        if prep1!=None:
                            # print("DSFN4三元组：（" + item1.lemma + "，" + pred.lemma + "" + prep1.lemma + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred.lemma + "" + prep1.lemma, item2.lemma])
                            # print("DSFN4三元组：（" + item1.lemma + "，" + pred2.lemma + "" + prep.lemma + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred2.lemma + "" + prep.lemma, item2.lemma])
                        else:
                            # print("DSFN4三元组：（" + item1.lemma + "，" + pred.lemma  + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred.lemma , item2.lemma])
                            # print("DSFN4三元组：（" + item1.lemma + "，" + pred2.lemma + "" + prep.lemma + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred2.lemma + "" + prep.lemma, item2.lemma])

        """
        DSFN5
        """
        # self.dsfn5and6(rawSentence,sentence,item1,item2)
        return allTripes

    def get_entity_num_between(self,verb1,verb2,sentence):
        """
        获得两个动词之间的实体数量
        Parameters
        ----------
        entity1 : WordUnit，动词1
        entity2 : WordUnit，动词2
        Returns：
            num：int，两动词间的实体数量
        """
        if verb1.ID > verb2.ID:
            c = verb1
            verb1 = verb2
            verb2 = c
        num = 0
        i = verb1.ID
        while i < verb2.ID-1:
            if self.is_entity(sentence.words[i]):
                num +=1
            i +=1
        return num

    def is_entity(self,entry):
        """判断词单元是否是实体
        Args：
            entry：WordUnit，词单元
        Returns：
            *:bool，实体（True），非实体（False）
        """
        #候选实体词性列表
        entity_postags = ['nh','ni','ns','nz','j','n','v']
        # print(entry.lemma+" : "+entry.postag)
        if entry.postag in entity_postags:
            return True
        else:
            return False
    def dsfnAttCOO(self,sentence,item1,item2):
        item1Att = item1
        item2Att = item2
        while item1Att.dependency == "ATT":
            item1Att = item1Att.head_word

        allTripe = self.dsfn1_2_3_4COO(sentence,item1Att,item2)
        if allTripe == None or len(allTripe) == 0:
            while item2Att.dependency == "ATT":
                item2Att = item2Att.head_word
            allTripe = self.dsfn1_2_3_4COO(sentence,item1,item2Att)
        if allTripe == None or len(allTripe) == 0:
            allTripe = self.dsfn1_2_3_4COO(sentence,item1Att,item2Att)
        for tripe in allTripe:
            if tripe[0] == item1Att.lemma:
                tripe[0] = item1.lemma
            if tripe[2] == item2Att.lemma:
                tripe[2] = item2.lemma
        return allTripe

    def dsfn5COO(self, sentence, item1, item2):
        if item1.dependency == "COO":
            item1COO = item1.head_word
            allTripes1 = self.dsfn1_2_3_4COO(sentence,item1COO,item2)
            # print(allTripes1)
            for tripe in allTripes1:
                if tripe[0] == item1COO.lemma:
                    tripe[0] = item1.lemma
                elif tripe[2] == item1COO.lemma:
                    tripe[2] = item1.lemma
            return allTripes1
            # print("allTripes1"+str(allTripes1))

    def dsfn6COO(self,sentence,item1,item2):
        if item2.dependency == "COO":
            item2COO = item2.head_word
            allTripes2 = self.dsfn1_2_3_4COO(sentence,item1,item2COO)
            for tripe in allTripes2:
                if tripe[2] == item2COO.lemma:
                    tripe[2] = item2.lemma
                elif tripe[0] == item2COO.lemma:
                    tripe[0] = item2.lemma
            return allTripes2

    def dsfn5and6COO(self,sentence,item1,item2):
        if item1.dependency == "COO":
            item1COO = item1.head_word
            if item2.dependency == "COO":
                item2COO = item2.head_word
                allTripe = self.dsfn1_2_3_4COO(sentence,item1COO,item2COO)
                for tripe in allTripe:
                    if tripe[0] == item1COO.lemma and tripe[2] == item2COO.lemma:
                        tripe[0] = item1.lemma
                        tripe[2] = item2.lemma
                    if tripe[2] == item1COO.lemma and tripe[0] == item2COO.lemma:
                        tripe[2] = item1.lemma
                        tripe[0] = item2.lemma
                return allTripe


    def dsfnStartCOO3(self, rawSentence, entity1, entity2):
        nounRelatedWithPosition = ['主席','总理','教授','校长']
        resultList = []
        lemmas = dsfn.segment(rawSentence)
        words = dsfn.postag(lemmas)
        words_netag = dsfn.netag(words)
        sentence = dsfn.parse(words_netag)
        # print(sentence.to_string())
        item1 = None
        item2 = None
        for item in sentence.words:
            if (item.lemma == entity1):
                item1 = item
            if (item.lemma == entity2):
                item2 = item
        if item1 == None or item2 == None:
            return None
        if item1.ID > item2.ID:
            c = item1
            item1 = item2
            item2 = c
        itemCopy1 = item1
        itemCopy2 = item2
        allTripes = self.dsfnStartCOO2(sentence,item1,item2)
        if allTripes!=None and len(allTripes) == 0:
            # return None
            if item1.postag in ['n', 'nh', 'nl', 'ns', 'nz', 'ni'] and item1.dependency == "ATT":
                item1 = item1.head_word
                while item1.dependency == "ATT":
                    item1 = item1.head_word
                if 'n' in item1.postag and item1.postag not in ['nh', 'ns', 'nz', 'ni']:
                    pass
                else:
                    item1 = itemCopy1

            if item2.postag in ['n', 'nh', 'nl', 'ns', 'nz', 'ni'] and item2.dependency == "ATT":
                item2 = item2.head_word
                while item2.dependency == "ATT":
                    item2 = item2.head_word
                if 'n' in item2.postag and item2.postag not in ['nh', 'ns', 'nz', 'ni']:
                    pass
                else:
                    item2 = itemCopy2
            allTripes = self.dsfnStartCOO2(sentence, item1, item2)
            # print("注意")
            # print(allTripes)
            if len(allTripes) != 0:
                for tripe in allTripes:
                    if tripe[1]!= "":
                        if tripe[0] == item1.lemma:
                            tripe[0] = itemCopy1.lemma
                        elif tripe[2] == item1.lemma:
                            tripe[2] = itemCopy1.lemma

                        if tripe[0] == item2.lemma:
                            tripe[0] = itemCopy2.lemma
                        elif tripe[2] == item2.lemma:
                            tripe[2] = itemCopy2.lemma
                        # print("12345")
                        resultList.append(tripe)
                # print("最终结果")
                # print(np.array(set([tuple(t) for t in resultList])))
                if len(resultList)>0:
                    return np.array(set([tuple(t) for t in resultList]))
        else:
            for tripe in allTripes:
                if tripe[1]!="":
                    resultList.append(tripe)
            if len(resultList) > 0:
                return np.array(set([tuple(t) for t in resultList]))


    def dsfnStartCOO2(self, sentence, item1, item2):
        nounRelatedWithPosition = ['主席', '总理', '教授', '校长']
        resultList = []
        itemCopy1 = item1
        itemCopy2 = item2
        """
        来解决ATT依赖的名词，如 李克强[ATT] <----- 总理[SBV]
        """
        # print(item1.lemma)
        # print(item2.lemma)
        allTripes = self.dsfn1_2_3_4COO(sentence, item1, item2)
        if len(allTripes) == 0:
            # print("11111111")
            allTripes = self.dsfn5COO(sentence, item1, item2)
            if allTripes == None or len(allTripes) == 0:
                # print("2222222")
                allTripes = self.dsfn6COO(sentence, item1, item2)
                if allTripes == None or len(allTripes) == 0:
                    # print("3333333")
                    allTripes = self.dsfn5and6COO(sentence, item1, item2)
                    # if allTripes == None or len(allTripes) == 0:
                    #     print("44444444444")
                    #     allTripes = self.dsfnAttCOO(sentence,item1,item2)
        # print("第一次"+str(allTripes))
        if allTripes != None and len(allTripes) != 0:
            for tripe in allTripes:
                resultList.append(tripe)
        # print("第二次")
        pred1 = None
        subForCoo = None
        for item in sentence.words:
            if item.postag == "v" and item.dependency == "COO":
                pred1 = item.head_word

                for word in sentence.words:
                    if word.dependency == "SBV" and word.head_word.ID == pred1.ID:
                        for phrase in sentence.words:
                            if phrase.dependency == "SBV" and phrase.head_word.ID == item.ID:
                                subForCoo = phrase
                        if subForCoo == None or (
                                subForCoo != None and subForCoo.ID == word.ID):  # 处理动词COO的情况，必须要保证此并列动词没有额外主语。
                            # 考虑到：习近平主席视察厦门，李克强总理访问香港
                            word.head_word = item
                            allTripes = self.dsfn1_2_3_4COO(sentence, item1, item2)
                            if len(allTripes) == 0:
                                # print("11111111")
                                allTripes = self.dsfn5COO(sentence, item1, item2)
                                if allTripes == None or len(allTripes) == 0:
                                    # print("2222222")
                                    allTripes = self.dsfn6COO(sentence, item1, item2)
                                    if allTripes == None or len(allTripes) == 0:
                                        # print("3333333")
                                        allTripes = self.dsfn5and6COO(sentence, item1, item2)
                                        # if allTripes == None or len(allTripes) == 0:
                                        #     allTripes = self.dsfnAttCOO(sentence,item1,item2)
                            # print("第二次"+str(allTripes))
                            if allTripes != None and len(allTripes) != 0:
                                for tripe in allTripes:
                                    resultList.append(tripe)
        # print(np.array(set([tuple(t) for t in resultList])))
        return resultList

"""
考虑到一句话越长，则LTP的效果越不好
"""
if __name__ == '__main__':
    dsfn = DSFN()
    # 分词测试
    print('***' + '分词测试' + '***')
    allSentence = []

    f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\' + "5A_颐和园.txt"
             , 'r', encoding='utf-8')
    file = f.read()
    #    print(file)
    json_file = json.loads(file)  # 转化为json格式
    text = json_file.get("text")  # 读取text
    sentence_list = dsfn.splitSentence(text)  # 将text分为句子列表
    print(sentence_list)
    # for sentence in sentence_list:
    #     for index1 in range(0,len(person)):
    #         if person[index1] not in sentence:
    #             continue
    #         for index2 in range(index1+1,len(person)):
    #             if person[index2] not in sentence:
    #                  continue
    #             # print(sentence+"----"+person[index1]+"----"+person[index2])
    #             tripes = dsfn.dsfnStartCOO3(sentence,person[index1],person[index2])
    #             # print(tripes)
    #             if tripes!=None  and tripes.size!=0:
    #                 print(sentence+" : "+person[index1]+"--"+person[index2])
    #                 print(tripes)
    f = open('..\\..\\entity_verb\\entity_verb_result\\' + "all_entity.json"
             , 'r', encoding='utf-8')
    file = f.read()
    all_entity = json.loads(file)['all_entity']
    for sentence in sentence_list:
        for index1 in range(0, len(all_entity)):
            if all_entity[index1] not in sentence:
                continue
            for index2 in range(index1 + 1, len(all_entity)):
                if all_entity[index2] not in sentence:
                    continue
                # print(sentence+"----"+person[index1]+"----"+person[index2])
                tripes = dsfn.dsfnStartCOO3(sentence, all_entity[index1], all_entity[index2])
                # print(tripes)
                if tripes != None and tripes.size != 0:
                    print(sentence + " : " + all_entity[index1] + "--" + all_entity[index2])
                    print(tripes)
    # print(allSentence)
    dsfn.close()

    # if item.ID != sentence.words[0].head_word.ID:
    #     print(item.head_word.ID)
    # else:
    #     print(0)
    # sob = sentence.words[]