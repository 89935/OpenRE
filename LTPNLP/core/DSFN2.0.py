# -*- coding: utf-8 -*-

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
        # segmentor_flag = self.segmentor.load(os.path.join(default_model_dir, 'cws.model'))
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
        print(netags)
        for netag in netags:
            print(netag)
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
                print("三元组：（" + item1.lemma + "，" + AttWordStr + "，" + item2.lemma + "）")
                allTripes.append([item1.lemma, AttWordStr, item2.lemma])
        """
        判断两个实体是否属于DSFN1的情况，并输出三元组
        """

        """
        考虑DSFN2的情况
        """
        if item1.dependency == "SBV" and item1.head_word.postag == "v":
            pred1 = item1.head_word
            predDict = dict()
            predDict[pred1.ID] = pred1.lemma

            if item2.dependency == "VOB"  and item2.head_word.postag == "v":
                pred2 = item2.head_word
                predDict[pred2.ID] = pred2.lemma
                if (len(predDict) == 1):
                    PredWordStr = ""
                    for i in predDict:
                        PredWordStr += predDict[i]
                    print("DSFN2三元组：（" + item1.lemma + "，" + PredWordStr + "，" + item2.lemma + "）")
                    allTripes.append([item1.lemma, PredWordStr, item2.lemma])
                    """
                    新加，为了考虑“习近平视察和访问上海”的情况
                    """
                if len(predDict) ==2:
                    num = self.get_entity_num_between(pred1,pred2,sentence)
                    flagSBV = True
                    flagVOB = True
                    for word in sentence.words:
                        if word.dependency == "SBV" and word.head_word.ID == pred2.ID:
                            flagSBV = False
                        if word.dependency == "VOB" and word.head_word.ID == pred1.ID:
                            flagVOB = False
                    print("pred1:"+pred1.lemma+",pred2:"+pred2.lemma+",num:"+str(num))
                    if num == 0 :
                        if flagVOB == True:
                            print("DSFN2三元组：（" + item1.lemma + "，" + pred1.lemma + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred1.lemma, item2.lemma])
                        if flagSBV == True:
                            print("DSFN2三元组：（" + item1.lemma + "，" + pred2.lemma + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred2.lemma, item2.lemma])



        """
        DSFN3.0
        """
        pred = None
        prep = None
        if item1.dependency == "SBV" and item1.head_word.postag == "v" and item2.dependency == "POB":
            pred = item1.head_word
            prep = item2.head_word
        elif item1.dependency == "FOB" and item2.dependency == "POB"  :  # 考虑介词为“被”的情况，如 “小王被小明所陷害”
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
                                if word.head_word!=None and word.dependency == "ATT" and word.head_word.ID == object.ID:
                                    objectDict[word.ID] = word
                            objectDict = sorted(objectDict.items(), key=lambda item: item[0])
                            objectStr = ""
                            for objectItem in objectDict:
                                objectStr += objectItem[1].lemma
                            print(
                                "DSFN3三元组：（" + item1.lemma + "，" + pred.lemma + "" + objectStr + "，" + item2.lemma + "）")
                            allTripes.append([item1.lemma, pred.lemma + "" + objectStr, item2.lemma])
                    if object == None:
                        print("DSFN3三元组：（" + item1.lemma + "，" + pred.lemma + "，" + item2.lemma + "）")
                        allTripes.append([item1.lemma, pred.lemma , item2.lemma])
        """
        DSFN4
        """
        pred = None
        prep = None
        prep1 = None
        pred2 = None
        if item1.dependency == "SBV" and item1.head_word.postag == "v" and item2.dependency == "POB":
            pred = item1.head_word
            prep = item2.head_word
            if prep.dependency == "CMP" and prep.head_word.postag == "v":
                pred2 = prep.head_word
                if pred2.ID == pred.ID:
                    print("DSFN4三元组：（" + item1.lemma + "，" + pred.lemma + "" + prep.lemma + "，" + item2.lemma + "）")
                    allTripes.append([item1.lemma, pred.lemma + "" + prep.lemma, item2.lemma])
                else :
                    num = self.get_entity_num_between(pred1, pred2, sentence)
                    flagSBV = True
                    flagVOB = True
                    for word in sentence.words:
                        if word.dependency == "SBV" and word.head_word.ID == pred2.ID:
                            flagSBV = False
                        if word.dependency == "VOB" and word.head_word.ID == pred.ID:
                            flagVOB = False
                    # print("pred1:"+pred1.lemma+",pred2:"+pred2.lemma+",num:"+str(num))
                    if num == 0:
                        flag = True
                        for word in sentence.words:
                            if word.dependency == "CMP" and word.head_word.ID == pred.ID:
                                prep1 = word
                        if prep1 != None:
                            if flagVOB == True:
                                # print("DSFN4三元组：（" + item1.lemma + "，" + pred.lemma + "" + prep1.lemma + "，" + item2.lemma + "）")
                                allTripes.append([item1.lemma, pred.lemma + "" + prep1.lemma, item2.lemma])
                            # print("DSFN4三元组：（" + item1.lemma + "，" + pred2.lemma + "" + prep.lemma + "，" + item2.lemma + "）")
                            if flagSBV == True:
                                allTripes.append([item1.lemma, pred2.lemma + "" + prep.lemma, item2.lemma])
                        else:
                            if flagVOB == True:
                                # print("DSFN4三元组：（" + item1.lemma + "，" + pred.lemma + "，" + item2.lemma + "）")
                                allTripes.append([item1.lemma, pred.lemma, item2.lemma])
                            if flagSBV == True:
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
        entity_postags = ['nh','ni','ns','nz','j','n','v','i']
        print(entry.lemma+" : "+entry.postag)
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
        print(sentence.to_string())
        for item in sentence.words:
            if (item.lemma == entity1):
                item1 = item
            if (item.lemma == entity2):
                item2 = item
        if item1.ID > item2.ID:
            c = item1
            item1 = item2
            item2 = c
        itemCopy1 = item1
        itemCopy2 = item2
        allTripes = self.dsfnStartCOO2(sentence,item1,item2)
        if allTripes!=None and len(allTripes) == 0:
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
                if ('n' in item2.postag or 'q' in item2.postag) and item2.postag not in ['nh', 'ns', 'nz', 'ni']:
                    pass
                else:
                    item2 = itemCopy2
            allTripes = self.dsfnStartCOO2(sentence, item1, item2)
            print("注意")
            print(allTripes)
            if len(allTripes) != 0:
                for tripe in allTripes:
                    if tripe[0] == item1.lemma:
                        tripe[0] = itemCopy1.lemma
                    elif tripe[2] == item1.lemma:
                        tripe[2] = itemCopy1.lemma

                    if tripe[0] == item2.lemma:
                        tripe[0] = itemCopy2.lemma
                    elif tripe[2] == item2.lemma:
                        tripe[2] = itemCopy2.lemma
                    print("12345")
                    resultList.append(tripe)
                print("最终结果")
                print(np.array(set([tuple(t) for t in resultList])))
        else:
            print("最终结果")
            print(np.array(set([tuple(t) for t in allTripes])))

    def dsfnStartCOO2(self, sentence, item1, item2):
        nounRelatedWithPosition = ['主席', '总理', '教授', '校长']
        resultList = []
        itemCopy1 = item1
        itemCopy2 = item2
        """
        来解决ATT依赖的名词，如 李克强[ATT] <----- 总理[SBV]
        """
        print(item1.lemma)
        print(item2.lemma)
        allTripes = self.dsfn1_2_3_4COO(sentence, item1, item2)
        if len(allTripes) == 0:
            print("11111111")
            allTripes = self.dsfn5COO(sentence, item1, item2)
            if allTripes == None or len(allTripes) == 0:
                print("2222222")
                allTripes = self.dsfn6COO(sentence, item1, item2)
                if allTripes == None or len(allTripes) == 0:
                    print("3333333")
                    allTripes = self.dsfn5and6COO(sentence, item1, item2)
                    # if allTripes == None or len(allTripes) == 0:
                    #     print("44444444444")
                    #     allTripes = self.dsfnAttCOO(sentence,item1,item2)
        # print("第一次"+str(allTripes))
        if allTripes != None and len(allTripes) != 0:
            for tripe in allTripes:
                resultList.append(tripe)
        print("第二次")
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

                            print(sentence.to_string())
                            allTripes = self.dsfn1_2_3_4COO(sentence, item1, item2)
                            if len(allTripes) == 0:
                                # print("11111111")
                                allTripes = self.dsfn5COO(sentence, item1, item2)
                                if allTripes == None or len(allTripes) == 0:
                                    # print("2222222")
                                    allTripes = self.dsfn6COO(sentence, item1, item2)
                                    if allTripes == None or len(allTripes) == 0:
                                        print("3333333")
                                        allTripes = self.dsfn5and6COO(sentence, item1, item2)
                                        # if allTripes == None or len(allTripes) == 0:
                                        #     allTripes = self.dsfnAttCOO(sentence,item1,item2)
                            # print("第二次"+str(allTripes))
                            if allTripes != None and len(allTripes) != 0:
                                for tripe in allTripes:
                                    # if tripe[0] == item1.lemma:
                                    #     tripe[0] = itemCopy1.lemma
                                    # elif tripe[2] == item1.lemma:
                                    #     tripe[2] = itemCopy1.lemma
                                    #
                                    # if tripe[0] == item2.lemma:
                                    #     tripe[0] = itemCopy2.lemma
                                    # elif tripe[2] == item2.lemma:
                                    #     tripe[2] = itemCopy2.lemma
                                    resultList.append(tripe)
        print(np.array(set([tuple(t) for t in resultList])))
        return resultList

"""
考虑到一句话越长，则LTP的效果越不好
"""
if __name__ == '__main__':
    dsfn = DSFN()
    # 分词测试
    print('***' + '分词测试' + '***')
    # sentence = u'交泰殿：位于乾清宫以北'

    # sentence = u'乾清宫：内廷中心建筑，位于乾清门以北'
    # dsfn.dsfnStartCOO3("清代皇帝，在每年春节都要亲笔御书大“福”字，赏赐给有功的王公大臣，以表示天子对臣下的恩宠", "春节", "皇帝")
    # dsfn.dsfnStartCOO3("1962年的一天，周恩来总理在当时的北京市副市长、著名红学家王昆仑等人的陪同下到恭王府视察", "王昆仑", "周恩来")
    #     dsfn.dsfnStartCOO3("后来，厉子嘉把许多宫廷菜配方和做法教给了儿子厉俊峰，然后又传给了孙子厉善麟", "厉子嘉", "厉善麟")
    # dsfn.dsfnStartCOO3("北京故宫博物院位于北京城中心，东西宽753米，南北长961米，占地面积723600余平方米，周围环以10米高的城墙和52米宽的护城河（筒子河）", "北京故宫", "北京城")
    # 颐和园占地面积达293公顷，主要由万寿山和昆明湖两部分组成

    # dsfn.dsfnStartCOO3("与1874年恭亲王率领王公大臣抵制圆明园重修工程不同", "恭亲王", "王公大臣")
    # dsfn.dsfnStartCOO3("画中的人物画均取材于中国古典名著", "人物画", "中国")
    # dsfn.dsfnStartCOO3("乾隆帝以治理京西水系为藉口下令拓挖西湖", "乾隆帝", "西湖")
    # dsfn.dsfnStartCOO3("昆明湖的西堤是仿照西湖的苏堤建造的", "昆明湖", "西湖")
    # dsfn.dsfnStartCOO3("乾隆四十年（1775年），擢御前侍卫，值乾清宫门，并兼正蓝旗满洲副都统", "乾隆", "御前侍卫")
    # dsfn.dsfnStartCOO3("永璘（1766 - 1820），爱新觉罗氏，乾隆皇帝的第十七子，与嘉庆皇帝同被孝仪纯皇后所生", "嘉庆皇帝", "孝仪纯皇后")
    # dsfn.dsfnStartCOO3("托马斯在肯德基吃早餐", "托马斯", "肯德基")
    # dsfn.dsfnStartCOO3("乔丹是美国职业篮球运动员，出生在纽约", "乔丹", "运动员")
    # dsfn.dsfnStartCOO3("牙买加运动员博尔特击败了美国选手加特林，在里约奥运会再次夺得金牌", "牙买加", "博尔特")
    # dsfn.dsfnStartCOO3("牙买加运动员博尔特击败了美国选手加特林，在里约奥运会再次夺得金牌", "美国", "加特林")
    # dsfn.dsfnStartCOO3("牙买加运动员博尔特击败了美国选手加特林，在里约奥运会再次夺得金牌", "加特林", "博尔特")
    # dsfn.dsfnStartCOO3("牙买加运动员博尔特击败了美国选手加特林，在里约奥运会再次夺得金牌", "美国", "博尔特")
    # dsfn.dsfnStartCOO3("牙买加运动员博尔特击败了美国选手加特林，在里约奥运会再次夺得金牌", "牙买加", "加特林")
    # dsfn.dsfnStartCOO3("牙买加运动员博尔特击败了美国选手加特林，在里约奥运会再次夺得金牌", "里约奥运会", "博尔特")
    #
    # dsfn.dsfnStartCOO3("同治重修圆明园遭到抵制慈禧修建颐和园却无人反对", "乾隆", "颐和园")
    # dsfn.dsfnStartCOO3("“教师节那天，习近平主席在北京八一学校看望师生", "习近平", "北京八一学校")
    # dsfn.dsfnStartCOO3("巴拿马在2017年与中国建立外交关系", "巴拿马", "中国")
    # dsfn.dsfnStartCOO3("哈德森在伦敦的郊区汉普斯特德出生", "哈德森", "伦敦")
    # dsfn.dsfnStartCOO3("哈德森在伦敦的郊区汉普斯特德出生", "哈德森", "汉普斯特德")
    # dsfn.dsfnStartCOO3("习近平主席访问奥巴马先生", "习近平", "奥巴马")
    # dsfn.dsfnStartCOO3("习近平主席视察厦门，李克强访问香港", "习近平", "厦门")
    # dsfn.dsfnStartCOO3("习近平主席视察厦门，李克强访问香港", "习近平", "香港")
    # dsfn.dsfnStartCOO3("习近平主席视察厦门，李克强访问香港", "李克强", "厦门")
    # dsfn.dsfnStartCOO3("习近平主席和李克强总理访问美国", "李克强", "美国")
    # dsfn.dsfnStartCOO3("习近平主席视察厦门，李克强总理访问香港", "李克强", "香港")#已解决
    # dsfn.dsfnStartCOO3("习近平主席访问美国和英国", "习近平", "英国")#已解决
    # dsfn.dsfnStartCOO3("1900年，八国联军攻入北京，颐和园再遭浩劫，园藏文物又被毁掠一空", "八国联军", "北京")
    # dsfn.dsfnStartCOO3("在变法期间（6月至9月间），慈禧一直住在颐和园", "慈禧", "颐和园")
    #
    dsfn.dsfnStartCOO3("中国文学家梁启超", "中国", "梁启超")

    # dsfn.dsfnStartCOO3("习近平视察并访问厦门", "习近平", "厦门")
    # dsfn.dsfnStartCOO3("习近平主席和李克强总理访问美国", "习近平", "美国")
    # dsfn.dsfnStartCOO3("习近平主席和李克强总理访问英国和美国", "李克强", "美国")
    # dsfn.dsfnStartCOO3("习近平主席访问英国和美国", "习近平", "美国")
    # dsfn.dsfnStartCOO3("习近平访问美国和英国", "习近平", "美国")
    # dsfn.dsfnStartCOO3("习近平访问美国和英国", "习近平", "英国")
    # dsfn.dsfnStartCOO3("厦门大学的校长朱崇实", "朱崇实", "厦门大学")
    # #
    # dsfn.dsfnStartCOO3("奥巴马毕业于哈佛大学","奥巴马","哈佛大学")
    # dsfn.dsfnStartCOO3("德国总理高克访问中国，并在同济大学发表演讲","德国","高克")
    # dsfn.dsfnStartCOO3("德国总理高克访问中国，并在同济大学发表演讲","中国","高克")
    # dsfn.dsfnStartCOO3("德国总理高克访问中国，并在同济大学发表演讲","高克","同济大学")
    # dsfn.dsfnStartCOO3("中国国家主席习近平对埃及进行国事访问和发表演讲", "习近平", "演讲")
    # dsfn.dsfnStartCOO3("中国国家主席习近平在埃及发表演讲并进行国事访问", "习近平", "埃及")
    # dsfn.dsfnStartCOO3("习近平主席和李克强总理对上海进行访问和视察","习近平","上海")
    # dsfn.dsfnStartCOO3("北京大学校长兼党委书记小王", "北京大学", "小王")
    # dsfn.dsfnStartCOO3("小王，北京大学的校长","北京大学","小王")
    # dsfn.dsfnStartCOO3("珍宝馆、石鼓馆和戏曲馆这三个常设展馆位于宁寿宫区内","珍宝馆","宁寿宫")
    # dsfn.dsfnStartCOO3("小明前往北京，并访问北京大学", "小明", "北京大学")
    # dsfn.dsfnStartCOO3("小明被刺客所暗杀", "小明", "刺客")
    # dsfn.dsfnStartCOO3("小明被小王所陷害", "小明", "小王")
    # dsfn.dsfnStartCOO3("小明被小王和小李所陷害", "小明", "小王")
    # dsfn.dsfnStartCOO3("小明被小王和小李所陷害", "小李", "小王")
    # dsfn.dsfnStartCOO3("小明被小王和小李所陷害", "小李", "小明")
    # dsfn.dsfnStartCOO3("小明被小王和小李所陷害", "小明", "小李")
    # dsfn.dsfnStartCOO3("小明和小刚被小王和小李所陷害","小刚","小李")
    # dsfn.dsfnStartCOO3("小明和小刚被小王和小李所陷害","小王","小刚")
    # dsfn.dsfnStartCOO3("奥巴马在清华大学毕业", "奥巴马", "清华大学")
    # dsfn.dsfnStartCOO3("小明和奥巴马毕业于清华大学", "小明", "清华大学")
    # dsfn.dsfnStartCOO3("小明和奥巴马毕业于清华大学", "奥巴马", "清华大学")
    # dsfn.dsfnStartCOO3("小明和奥巴马毕业于清华大学和北京大学", "小明", "北京大学")
    # dsfn.dsfnStartCOO3("小明和奥巴马毕业于清华大学和北京大学", "北京大学", "奥巴马")
    # dsfn.dsfnStartCOO3("奥巴马出生在美国，成长于非洲", "奥巴马", "美国")
    # dsfn.dsfnStartCOO3("奥巴马出生在美国，成长于非洲", "奥巴马", "非洲")
    # dsfn.dsfnStartCOO3("奥巴马和小明出生并且成长于美国", "小明", "美国")
    # dsfn.dsfnStartCOO3("奥巴马和小明出生于并且成长于美国", "小明", "美国")
    # dsfn.dsfnStartCOO3("“佩奇和布林在1996年创建谷歌", "佩奇", "谷歌")
    # dsfn.dsfnStartCOO3("佩奇、小明、布林在1996年创建谷歌", "布林", "谷歌")
    # dsfn.dsfnStartCOO3("中国国家主席习近平访问上海","习近平","上海")
    # dsfn.dsfnStartCOO3("习近平和李克强访问并视察上海","习近平","上海")
    # dsfn.dsfnStartCOO3("习近平和李克强访问并视察上海","李克强","上海")
    # dsfn.dsfnStartCOO3("习近平和李克强访问并视察上海和北京","李克强","北京")
    # dsfn.dsfnStartCOO3("习近平和李克强访问并视察上海和北京","习近平","北京")
    # dsfn.dsfnStartCOO3("习近平对北京进行视察,并参观故宫","习近平","故宫")
    # dsfn.dsfnStartCOO3("小王和小明对埃及和泰国进行了国事访问","小王","泰国")
    # dsfn.dsfnStartCOO3("小王和小明对埃及进行了国事访问","小明","埃及")
    #
    # dsfn.dsfnStartCOO3("中国的国家主席习近平","中国","习近平")
    # # # 恭王府以前的主人是大奸相和珅，他修建了庆颐堂，模仿了皇帝的宁寿宫
    # dsfn.dsfnStartCOO3("恭王府的主人奕䜣，是一等贵族，所以他的府邸不仅宽大，而且建筑也是最高格制","恭王府","奕䜣")
    # dsfn.dsfnStartCOO3("德国总理高克访问上海，并在同济大学发表演讲","德国","高克")
    # dsfn.dsfnStartCOO3("德国总理高克访问上海，并在同济大学发表演讲", "德国", "上海")#错误
    # # #
    # dsfn.dsfnStartCOO3("德国总理高克对上海进行访问，并在北京大学发表演讲", "上海", "高克")
    # dsfn.dsfnStartCOO3("德国总理高克对上海进行访问，并在北京大学发表演讲", "北京大学", "高克")#已解决
    # dsfn.dsfnStartCOO3("德国总理高克访问上海，并发表演讲", "上海", "高克")  # 已解决

    # dsfn.dsfnStartCOO("中国国家主席习近平对埃及进行国事访问和发表演讲", "习近平", "埃及")
    # dsfn.dsfnStartCOO("中国国家主席习近平在埃及发表演讲并进行国事访问", "习近平", "埃及")
    # dsfn.dsfnStart("习近平主席和李克强总理对上海进行访问和视察","习近平","上海")
    # dsfn.dsfnStart("北京大学校长兼党委书记小王", "北京大学", "小王")
    # dsfn.dsfnStart("小王，北京大学的校长","北京大学","小王")
    # dsfn.dsfnStart("珍宝馆、石鼓馆和戏曲馆这三个常设展馆位于宁寿宫区内","珍宝馆","宁寿宫")
    # dsfn.dsfnStartCOO("小明前往北京，并访问北京大学", "小明", "北京大学")
    # dsfn.dsfnStart("小明被刺客所暗杀", "小明", "刺客")
    # dsfn.dsfnStartCOO("小明被小王所陷害", "小明", "小王")
    # dsfn.dsfnStart("小明被小王和小李所陷害", "小明", "小王")
    # dsfn.dsfnStart("小明被小王和小李所陷害", "小李", "小王")
    # dsfn.dsfnStart("小明被小王和小李所陷害", "小李", "小明")
    # dsfn.dsfnStart("小明被小王和小李所陷害", "小明", "小李")
    # dsfn.dsfnStart("小明和小刚被小王和小李所陷害","小刚","小李")
    # dsfn.dsfnStartCOO("小明和小刚被小王和小李所陷害","小王","小刚")
    # dsfn.dsfnStart("奥巴马在清华大学毕业", "奥巴马", "清华大学")
    # dsfn.dsfnStart("小明和奥巴马毕业于清华大学", "小明", "清华大学")
    # dsfn.dsfnStart("小明和奥巴马毕业于清华大学", "奥巴马", "清华大学")
    # dsfn.dsfnStart("小明和奥巴马毕业于清华大学和北京大学", "小明", "北京大学")
    # dsfn.dsfnStart("小明和奥巴马毕业于清华大学和北京大学", "北京大学", "奥巴马")
    # dsfn.dsfnStartCOO("奥巴马出生在美国，成长于非洲", "奥巴马", "美国")
    # dsfn.dsfnStartCOO("奥巴马出生在美国，成长于非洲", "奥巴马", "非洲")
    # dsfn.dsfnStartCOO("奥巴马和小明出生并且成长于美国", "小明", "美国")
    # dsfn.dsfnStartCOO("奥巴马和小明出生于并且成长于美国", "小明", "美国")
    # dsfn.dsfnStart("“佩奇和布林在1996年创建谷歌", "佩奇", "谷歌")
    # dsfn.dsfnStart("佩奇、小明、布林在1996年创建谷歌", "布林", "谷歌")
    # dsfn.dsfnStart("中国国家主席习近平访问上海","习近平","上海")
    # dsfn.dsfnStartCOO("习近平访问并视察上海","习近平","上海")
    # dsfn.dsfnStartCOO("习近平对上海进行视察,并参观故宫","习近平","故宫")
    # dsfn.dsfnStart("小王和小明对埃及和泰国进行了国事访问","小王","泰国")
    # dsfn.dsfnStart("小王和小明对埃及进行了国事访问","小明","埃及")
    # dsfn.dsfnStart("中国的国家主席习近平","中国","习近平")
    # # 恭王府以前的主人是大奸相和珅，他修建了庆颐堂，模仿了皇帝的宁寿宫
    # dsfn.dsfnStart("恭王府的主人奕䜣，是一等贵族，所以他的府邸不仅宽大，而且建筑也是最高格制","恭王府","奕䜣")
    # dsfn.dsfnStart("德国总理高克访问上海，并在同济大学发表演讲","德国","高克")
    # dsfn.dsfnStart("德国总理高克访问上海，并在同济大学发表演讲", "德国", "上海")#错误
    #
    # dsfn.dsfnStartCOO("德国总理高克对上海进行访问，并在北京大学发表演讲", "上海", "高克")
    # dsfn.dsfnStartCOO("德国总理高克对上海进行访问，并在北京大学发表演讲", "北京大学", "高克")#已解决
    # dsfn.dsfnStartCOO("德国总理高克访问上海，并发表演讲", "上海", "高克")  # 已解决




    # dsfn.whichdsfn("中国国家主席习近平对埃及进行国事访问和发表演讲", "习近平", "埃及")
    # dsfn.whichdsfn("中国国家主席习近平对上海进行访问和视察","习近平","上海")
    # dsfn.whichdsfn("小明被刺客所暗杀", "小明", "刺客")
    # dsfn.whichdsfn("小明被小王所陷害", "小明", "小王")
    # dsfn.whichdsfn("奥巴马在清华大学毕业", "奥巴马", "清华大学")
    # dsfn.("小明和奥巴马毕业于清华大学", "小明", "清华大学")
    # dsfn.whichdsfn("小明和奥巴马毕业于清华大学", "奥巴马", "清华大学")
    # dsfn.whichdsfn("小明和奥巴马毕业于清华大学和北京大学", "小明", "北京大学")
    # dsfn.whichdsfn("小明和奥巴马毕业于清华大学和北京大学", "奥巴马", "北京大学")
    # dsfn.whichdsfn("奥巴马出生并且成长于美国", "奥巴马", "美国")
    # dsfn.whichdsfn("“佩奇和布林在1996年创建谷歌", "佩奇", "谷歌")
    # dsfn.whichdsfn("佩奇、小明、布林在1996年创建谷歌", "布林", "谷歌")
    # dsfn.whichdsfn("中国国家主席习近平访问上海","习近平","上海")
    # dsfn.whichdsfn("习近平访问并视察上海","习近平","上海")
    # dsfn.whichdsfn("小王和小明对埃及进行了国事访问","小王","埃及")
    # dsfn.whichdsfn("小王和小明对埃及进行了国事访问","小明","埃及")
    # dsfn.whichdsfn("中国的国家主席习近平","中国","习近平")
    # # 恭王府以前的主人是大奸相和珅，他修建了庆颐堂，模仿了皇帝的宁寿宫
    # dsfn.whichdsfn("恭王府的主人奕䜣，是一等贵族，所以他的府邸不仅宽大，而且建筑也是最高格制","恭王府","奕䜣")
    dsfn.close()

    # if item.ID != sentence.words[0].head_word.ID:
    #     print(item.head_word.ID)
    # else:
    #     print(0)
    # sob = sentence.words[]