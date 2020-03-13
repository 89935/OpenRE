# -*- coding: utf-8 -*-
# SPO针对实体处理了一下
# import pynlpir
from pyltp import Segmentor, Postagger, NamedEntityRecognizer, Parser
import os

from LTPNLP.core.mapEntity import mapEntity
from entity_verb.entity_verb_new import entity_verb_new
import sys

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
    location_entity = ["中和殿", "太庙", "人文地理", "亚运村", "九龙壁", "圆明园", "古典建筑", "庑殿顶", "天井", "无量殿", "慈宁宫", "三希堂", "居庸关", "延寿寺", "排云殿", "东桥", "圜丘", "南天门", "垂花门", "西六宫", "配楼", "柳荫街", "中国四大名园", "午门", "乾东五所", "建筑管理", "世界博物馆", "西什库教堂", "晚清", "万泉河", "东暖阁", "储秀宫", "西华门", "院落", "地安门东大街", "御路", "知鱼桥", "清宁宫", "金水河", "景山前街", "司马台长城", "景山公园", "乐寿堂", "东六宫", "延陵", "宜芸馆", "芍药居", "承乾宫", "琉璃瓦", "湘江", "敌楼", "安定门外大街", "三音石", "崇文门", "天坛路", "台基", "东城区", "外朝", "武备", "全国重点文物保护单位", "房山石", "静园", "香山", "中东", "坤宁宫", "彩画", "江南园林", "北河沿大街", "岳阳楼", "丽景轩", "巴黎圣母院", "钟表馆", "戏楼", "白银", "红海", "中原", "明长城", "神乐署", "瀛洲", "码头", "百度地图", "旋子彩画", "乾西五所", "天圆地方", "琉璃厂文化街", "广岛", "御沟", "井亭", "古柏林", "石坊", "北京故宫", "宝云阁", "甬道", "熙和门", "乾清门", "北京城", "暖温带", "沥粉贴金", "安定路", "北齐长城", "减柱造", "宅园", "清华园", "天坛东门站", "西苑", "土山", "温带季风气候", "宫古", "东直门", "美国国务卿", "北海", "中华梦石城", "东门站", "天坛公园", "江山", "谐趣园", "修宅", "苏堤", "玉泉", "牌坊", "蓟镇", "高速公路", "钟粹宫", "无梁殿", "政治家", "牌楼", "波斯", "西内", "老龙头", "阴阳石", "三神山", "丹陛桥", "中国第一历史档案馆", "建筑艺术", "四川", "护城河", "文华殿", "静宜园", "乐峰", "永和宫", "金砖", "清漪园", "安定门", "宫殿", "梵华楼", "龙井", "水街", "东华门", "歇山式顶", "斋宫", "渤海镇", "仁和", "白浮村", "建筑风格", "买卖街", "藻鉴堂", "寿安宫", "奉先殿", "后海", "宋", "承德避暑山庄", "前门站", "寿安山", "八达岭", "棂星门", "经幢", "泰山", "后三宫", "天桥商场", "维新派", "拙政园", "北京十六景", "南湖岛", "山寨", "东海", "寺庙", "图书馆", "西山", "延禧宫", "九土", "十七孔桥", "鹊桥", "石鼓", "样式雷", "礼乐", "圆石", "动物园", "西湖", "齐长城遗址", "京畿", "正脊", "神武门", "洛神赋图", "绿地面积", "暖阁", "多宝塔", "磨砖对缝", "湖心亭", "崇楼", "五谷丰登", "养性殿", "关山", "砖雕", "北境", "凤凰墩", "金殿", "永定路", "世界遗产", "古柏", "郡王府", "慕田峪", "皇舆全览图", "古典园林", "坐北朝南", "皇极殿", "皇家园林", "东四十条", "京西", "黄花镇", "通惠河", "宁寿宫", "旅游局", "大角楼", "昆明湖", "后溪", "东堤", "汉白玉石", "皇史宬", "湖心岛", "长春宫", "玉澜堂", "紫檀", "玉泉山", "玉山", "茶楼", "敌台", "乾清宫", "巴县", "藕香榭", "斗拱", "苏州街", "紫禁城", "颐和轩", "皇穹宇", "南方", "智慧海", "八小部洲", "拱券", "门楣", "太和殿", "銮仪卫", "法门寺地宫", "清音阁", "龙王庙", "城岛", "皇陵", "筒瓦", "天地坛", "张古", "建筑史", "武英殿", "北长街", "天坛", "云山", "大石桥", "北平", "宫殿建筑", "山东", "博物馆", "昆明池", "交道口南大街", "平流村", "聊城", "三大殿", "清晏舫", "墀头", "养心殿", "御道", "百花园", "翊坤宫", "神道", "落地罩", "渔村", "丹陛", "歇山顶", "畅音阁", "漱芳斋", "黄鹤楼", "柱础", "嘉乐堂", "庆长", "档案", "保定", "上海", "佛香阁", "望柱", "德和园", "天桥", "北京旅游网", "祈年殿", "颐和园", "攒尖顶", "香岩宗印之阁", "分界线", "大杂院", "交泰殿", "太和门", "南郊", "健翔桥", "瓮山", "勤政殿", "云南", "景仁宫", "小山村", "金水桥", "保和殿", "寄畅园", "珍妃井", "德和园大戏楼", "正房", "第一批全国重点文物保护单位", "三合院", "万寿山", "厉家菜", "玉峰塔", "藻井", "恭王府花园", "文昌阁", "景山", "前门东大街", "端门", "代王府", "万寿亭", "景阳宫", "东四环", "景明楼", "祈谷坛", "大戏楼", "安佑宫", "石舫", "流杯亭", "行宫", "法华寺", "圜丘坛", "正义路", "居庸关长城", "箭扣长城", "石牌坊", "回音壁", "和玺彩画", "二龙戏珠", "北四环", "玉龙", "广州", "盛京", "四合院", "曲尺", "谷仓", "永定门", "宝顶", "苏式彩画", "皇宫", "寿康宫"]
    def __init__(self, model_dir=default_model_dir, all_entity=all_entity):
        self.default_model_dir = model_dir
        # 加载ltp模型
        #
        default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\'  # LTP模型文件目录
        self.segmentor_user = Segmentor()
        user_dict = "..\\source\\user.txt"
        segmentor_flag_user = self.segmentor_user.load_with_lexicon(os.path.join(default_model_dir, 'cws.model'), user_dict)
        self.segmentor = Segmentor()
        segmentor_flag = self.segmentor.load(os.path.join(default_model_dir, 'cws.model'))
        # 词性标注模型
        self.postagger = Postagger()
        postag_flag = self.postagger.load(os.path.join(self.default_model_dir, 'pos.model'))
        # 命名实体识别模型
        self.recognizer = NamedEntityRecognizer()
        ner_flag = self.recognizer.load(os.path.join(self.default_model_dir, 'ner.model'))
        # 依存句法分析模型
        self.parser = Parser()
        parser_flag = self.parser.load(os.path.join(self.default_model_dir, 'parser.model'))

        if segmentor_flag or postag_flag or ner_flag or parser_flag or segmentor_flag_user:  # 可能有错误
            print('load model failed')

    def segment(self, sentence, segmentor, entity_postag=dict()):
        words = segmentor.segment(sentence)
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

    def splitSentenceByComma(self,text):
        pattern = r'，'
        result_list = re.split(pattern, text)
        result_list = list(filter(self.not_empty, result_list))
        final_list = []
        for sentence in result_list:
            if len(sentence) <= 40:
                final_list.append(sentence)
        return final_list

    def not_empty(self,s):
        return s and "".join(s.split())

    def dsfn1_2_3_4COO(self, sentence, item1, item2):
        allTripes = []

        """
        判断两个实体是否属于DSFN1的情况，并输出三元组
        """
        # location_position_list = ['主席','总统','总理','主任','内','东门','西门','南门','北门','大门','外','国家主席','尚书'
        #                           ]
        """
        去除约束2
        """
        if  (item1.dependency == "ATT"):
            AttWord = item1.head_word
            AttWordDict = dict()
            AttWordStr = ""
            while AttWord.ID < item2.ID:
                AttWordDict[AttWord.ID] = AttWord.lemma
                # AttWordStr += AttWord.lemma
                if (AttWord.dependency == "ATT"  ):
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
                # if AttWordStr in location_position_list:
                allTripes.append([item1.lemma, AttWordStr, item2.lemma])


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
        entity_postags = ['nh','ni','ns','nz','j','n','v','m']
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
    def dsfnStart(self, rawSentence,segmentor, entity1, entity2,all_entity):
        nounRelatedWithPosition = ['主席','总理','教授','校长']
        resultList = []
        lemmas = dsfn.segment(rawSentence,segmentor)
        words = dsfn.postag(lemmas)
        words_netag = dsfn.netag(words)
        sentence = dsfn.parse(words_netag)
        # print(sentence.to_string())
        Rawitem1 = None
        Rawitem2 = None
        item1 = None
        item2 = None
        Rawitem1Index = -1
        Rawitem2Index = -1
        indexList = [-1,-1]
        for item in sentence.words:
            if (item.lemma == entity1):
                Rawitem1 = item
            if (item.lemma == entity2):
                Rawitem2 = item
            if Rawitem1 != None and Rawitem2 != None and (Rawitem1.ID!=Rawitem1Index or Rawitem2.ID!=Rawitem2Index):
                Rawitem1Index = Rawitem1.ID
                Rawitem2Index = Rawitem2.ID
                # if item1 == None or item2 == None:
                #     return None
                item1 = Rawitem1
                item2 = Rawitem2
                if item1.ID > item2.ID:
                    c = item1
                    item1 = item2
                    item2 = c
                # print(str(item1.ID) + "   " + str(item2.ID))
                itemCopy1 = item1
                itemCopy2 = item2
                # print(item1.lemma)
                # print(item2.lemma)
                # print(self.dsfnConstraints2(sentence,item1,item2,all_entity))
                if self.dsfnConstraints2(sentence,item1,item2,all_entity) == False:

                    continue
                allTripes = self.dsfnStartCOO2(sentence,item1,item2)
                # print("111"+item2.lemma)
                # print(allTripes)
                if allTripes == None or (allTripes!=None and len(allTripes) == 0):
                    # print("我要走ATT的部分了")
                    while item1.dependency == "ATT":
                        item1 = item1.head_word
                    while item2.dependency == "ATT":
                        item2 = item2.head_word
                    allTripes = self.dsfnStartCOO2(sentence, item1, item2)
                    if len(allTripes) != 0:
                        for tripe in allTripes:
                            if tripe[1]!= "":
                                if tripe[0] == item1.lemma:
                                    if item1.ID < itemCopy1.ID:
                                        tripe[0] = item1.lemma+""+itemCopy1.lemma
                                    elif item1.ID > itemCopy1.ID:
                                        tripe[0] = itemCopy1.lemma+""+item1.lemma
                                    else:
                                        tripe[0] = itemCopy1.lemma

                                elif tripe[2] == item1.lemma:
                                    if item1.ID < itemCopy1.ID:
                                        tripe[2] = item1.lemma+""+itemCopy1.lemma
                                    elif item1.ID > itemCopy1.ID:
                                        tripe[2] = itemCopy1.lemma+""+item1.lemma
                                    else:
                                        tripe[2] = itemCopy1.lemma
                                    # tripe[2] = itemCopy1.lemma

                                if tripe[0] == item2.lemma:
                                    if item2.ID < itemCopy2.ID:
                                        tripe[0] = item2.lemma + ""+ itemCopy2.lemma
                                    elif item2.ID > itemCopy2.ID:
                                        tripe[0] = itemCopy2.lemma + ""+ item2.lemma
                                    else:
                                        tripe[0] = itemCopy2.lemma
                                elif tripe[2] == item2.lemma:
                                    # print(item2.lemma)
                                    if item2.ID < itemCopy2.ID:
                                        tripe[2] = item2.lemma + ""+ itemCopy2.lemma
                                    elif item2.ID > itemCopy2.ID:
                                        tripe[2] = itemCopy2.lemma + ""+ item2.lemma
                                    else:
                                        tripe[2] = itemCopy2.lemma
                                # print("12345")
                                resultList.append(tripe)
                else:
                    for tripe in allTripes:
                        if tripe[1]!="":
                            resultList.append(tripe)
                    # if len(resultList) > 0:
                    #     return np.array(set([tuple(t) for t in resultList]))
        if item1 == None or item2 == None:
            return None
        if len(resultList) > 0:
            # return np.array(set([tuple(t) for t in resultList]))
            # print("输出结果1"+str(resultList))
            return resultList
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
                            # print(sentence.to_string())
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
                                        #     allTripes = self.dsfnAttCOO(sentence,item1,item2)
                            # print("第二次"+str(allTripes))
                            if allTripes != None and len(allTripes) != 0:
                                for tripe in allTripes:
                                    resultList.append(tripe)
        # print(np.array(set([tuple(t) for t in resultList])))
        return resultList

    def dsfnConstraints1(self,rawSentence,maxLength):
        """
        :param rawSentence: 原句子
        :param maxLength: 句子的最大长度
        :return: 小于maxLength的长度
        """
        newSentence = []

        if len(rawSentence) <= maxLength:
            newSentence.append(rawSentence)
            return newSentence
        else:
            newSentence = self.splitSentenceByComma(rawSentence)
            return newSentence

    def dsfnConstraints2(self,sentence,item1,item2,allEntities):
        countEntity = 0
        countChar = 0
        for index in range(item1.ID+1, item2.ID):
            word = sentence.get_word_by_id(index)
            countChar += len(word.lemma)
            if word.lemma in allEntities:
                countEntity +=1
        # print(countEntity)
        # print(countChar)
        if countEntity > 3:
            return False
        elif countChar > 12:
            # print(countChar)
            return False
        else:
            return True

    def dsfnConstraints3(self,sentence,item1,item2):
        countChar = 0
        for index in range(item1.ID+1, item2.ID):
            word = sentence.get_word_by_id(index)
            countChar += len(word.lemma)
        if countChar > 5:
            return False
        else:
            return True

    def getSPO(self,sentence,segmentor):
        all_result = []
        raw_sentence = []
        RawSentence = sentence
        lemmas = self.segment(sentence,segmentor)
        words = self.postag(lemmas)
        words_netag = self.netag(words)
        sentence = self.parse(words_netag)
        # print(sentence.to_string())
        for itemWord in sentence.words:
            #来找到一个动词，这个动词要么是一句话的HED，要么与一句话的HED是COO的依存关系
            if (itemWord.head_word == None and itemWord.postag == "v" ) or (itemWord.postag == "v" and
                                                                  itemWord.dependency == "COO" and itemWord.head_word.head_word == None)\
                     or (itemWord.postag == "v") :
                relation_verb = itemWord   #将找到的这个动词，作为relation_verb
                relationString = relation_verb.lemma
                # print(relationString)
                if itemWord.head_word==None:
                    # print("1")
                    verbId = itemWord.ID   #关系动词的ID
                    verbId2 = None
                elif itemWord.head_word.head_word == None:
                    # print("2")

                    verbId = itemWord.ID   #该关系动词的ID
                    if itemWord.dependency == "COO" or self.get_entity_num_between(itemWord,itemWord.head_word,sentence)==0:
                        verbId2 = itemWord.head_word.ID  # 这句话的HED，用来找SUB
                    else:
                        verbId2 = None
                else:
                    # print("3")
                    verbId = itemWord.ID   #该关系动词的ID
                    verbId2 = None
                O_dict = dict() #存储所有的Object
                S_dict = dict() #存储所有的Subject
                verb_dict = dict() #存储所有的verb，主要考虑的情况为：习近平主席在北京大学发表演讲
                OBJ = None
                SUB = None
                DSFN3 = dict()
                for item in sentence.words:
                    if item.dependency == "SBV" and item.head_word.ID == verbId: #寻找这个动词的主语
                        # if SUB == None or SUB.lemma != entity:
                        SUB = item #找到主语
                        S_dict[SUB.ID] = SUB.lemma #将主语加入到字典中

                    if (item.dependency == "VOB" and item.head_word.ID == verbId and item.postag!= "v"):
                        # 找到这个动词的宾语，其中包括：直接宾语，介词宾语（该宾语依赖POB---->介词(词性为p)--ADV or CMP-->动词）
                        OBJ = item
                        O_dict[OBJ.ID] = OBJ.lemma
                        relationString = relation_verb.lemma
                        verb_dict[OBJ.ID] = relationString
                    if (item.dependency == "POB" and item.head_word.postag == "p" and item.head_word.dependency == "CMP"
                                and item.head_word.head_word.ID== verbId ) :
                        # 找到这个动词的宾语，其中包括：直接宾语，介词宾语（该宾语依赖POB---->介词(词性为p)--ADV or CMP-->动词）
                        OBJ = item
                        O_dict[OBJ.ID] = OBJ.lemma
                        relationString = relation_verb.lemma + "" + item.head_word.lemma
                        verb_dict[OBJ.ID] = relationString

                    if (item.dependency == "POB" and (item.head_word.postag == "p" or item.head_word.postag == 'd')\
                            and item.head_word.dependency == "ADV" and item.head_word.head_word.ID == verbId \
                            and item.postag!='v'):
                        # 找到这个动词的宾语，其中包括：直接宾语，介词宾语（该宾语依赖POB---->介词(词性为p)--ADV or CMP-->动词）
                        OBJ = item
                        O_dict[OBJ.ID] = OBJ.lemma
                        verbObj = None
                        DSFN3[OBJ.ID] = True
                        objectDict = dict()
                        relationString = relation_verb.lemma
                        for eachWord in sentence.words:
                            if eachWord.dependency == "VOB" and eachWord.head_word.ID == relation_verb.ID:
                                # relationString = relation_verb.lemma + "" + eachWord.lemma
                                verbObj = eachWord
                                objectDict[verbObj.ID] = verbObj
                        if verbObj != None:
                            for word in sentence.words:
                                if word.head_word != None and word.dependency == "ATT" and word.head_word.ID == verbObj.ID:
                                    objectDict[word.ID] = word
                            objectDict = sorted(objectDict.items(), key=lambda item: item[0])
                            objectStr = ""
                            for objectItem in objectDict:
                                objectStr += objectItem[1].lemma
                            relationString = relation_verb.lemma + "" + objectStr

                        else:
                            for eachWord in sentence.words:
                                if eachWord.dependency == "POB" and eachWord.head_word.dependency == "CMP" and\
                                    eachWord.head_word.head_word.ID == relation_verb.ID:
                                    relationString = relation_verb.lemma+""+eachWord.head_word.lemma+""+eachWord.lemma

                        verb_dict[OBJ.ID] = relationString


                if SUB == None:#如果没找到主语，那么就找与该动词并列的verbId2的主语
                    for item in sentence.words:
                        if item.dependency == "SBV" and item.head_word.ID == verbId2:
                            # if SUB == None or SUB.lemma != entity:
                            SUB = item
                            S_dict[SUB.ID] = SUB.lemma
                # print(verbId2)
                if OBJ == None:
                    verb_coo = None
                    for item in sentence.words:
                        if item.dependency == "COO" and item.head_word.ID == verbId and item.ID > verbId:
                            verb_coo = item
                            break
                    flag = True
                    if verb_coo != None and self.get_entity_num_between(relation_verb,verb_coo,sentence) == 0:

                        for item in sentence.words:
                            if item.dependency == "SBV" and item.head_word.ID == verb_coo.ID:
                                flag = False
                        if flag!= False:
                            for item in sentence.words:
                                if (item.dependency == "VOB" and item.head_word.ID == verb_coo.ID)\
                                        or (item.dependency == "POB" and item.head_word.postag == "p" and item.head_word.dependency == "CMP"
                                and item.head_word.head_word.ID== verb_coo.ID) or (item.dependency == "POB" and item.head_word.postag == "p"\
                        and item.head_word.dependency == "ADV" and item.head_word.head_word.ID== verb_coo.ID):

                                    OBJ = item
                                    O_dict[OBJ.ID] = OBJ.lemma
                # print(S_dict)
                # print(verb_dict)
                # print(O_dict)
                SUB_COO = None
                OBJ_COO = None
                for item in sentence.words:
                    if item.head_word != None:
                        if SUB != None and item.dependency == "COO" and item.head_word.ID  in S_dict: #获得主语的COO
                            SUB_COO = item
                            S_dict[SUB_COO.ID] = SUB_COO.lemma
                    if item.head_word != None and OBJ!=None:
                        if item.dependency == "COO" and item.head_word.ID in O_dict: #获得宾语的COO
                            OBJ_COO = item
                            O_dict[OBJ_COO.ID] = OBJ_COO.lemma
                S_new = []

                for sub in S_dict:
                    # if sentence.get_word_by_id(sub).postag == 'r':
                    #     continue
                    S_dict2 = dict()  # 存放主语ATT的列表
                    S_dict2[sub] = S_dict[sub]
                    flag = True
                    while flag == True:
                        len1 = len(S_dict2)
                        for item in sentence.words:
                            if item.head_word != None:
                                SUBList = S_dict2.keys()
                                if item.head_word.ID in SUBList and (item.dependency == "ATT" or item.dependency == "ADV"):
                                    SUBATT = item
                                    S_dict2[SUBATT.ID] = SUBATT.lemma

                            if len(S_dict2) != len1 :
                                flag = True
                            else:
                                flag = False
                    S_dict2 = sorted(S_dict2.items(), key=lambda item: item[0])
                    Subject = ""
                    for i in S_dict2:
                        Subject += i[1]
                    S_new.append(Subject)

                O_new = []
                V_new = []
                for obj in O_dict:
                    # if sentence.get_word_by_id(obj).postag == 'r':
                    #     continue
                    O_dict2 = dict()  # 存放宾语ATT的列表
                    O_dict2[obj] = O_dict[obj]
                    if verb_dict!=None:
                        if obj in verb_dict:
                            relationString2  = verb_dict[obj]
                        else:
                            relationString2 = relation_verb.lemma
                    else:
                        relationString2 = relation_verb.lemma
                    V_new.append(relationString2)
                    flag = True
                    while flag == True:
                        len2 = len(O_dict2)
                        for item in sentence.words:
                            if item.head_word != None:
                                OBJList = O_dict2.keys()
                                if item.head_word.ID in OBJList and (item.dependency == "ADV" or item.dependency == "ATT" or item.dependency == "VOB"
                                        or (item.dependency == "COO" and item.head_word.ID != obj)):
                                    if item.dependency == "ATT" and item.postag == "v":
                                        if self.get_entity_num_between(item,sentence.get_word_by_id(obj),sentence)>0:
                                            continue
                                        else:
                                            OBJATT = item
                                            O_dict2[OBJATT.ID] = OBJATT.lemma
                                    else:
                                        OBJATT = item
                                        O_dict2[OBJATT.ID] = OBJATT.lemma
                                        # print(OBJATT.lemma)

                            if len(O_dict2) != len2:
                                flag = True
                            else:
                                flag = False #一直循环，直到找不到新的修饰词
                    O_dict2 = sorted(O_dict2.items(), key=lambda item: item[0])
                    Object = ""
                    for i in O_dict2:
                        Object += i[1]
                    flag = False
                    # if obj in DSFN3:
                    #     for location in self.location_entity:
                    #         if location in Object :
                    #             flag = True
                    #     if flag == True:
                    #         O_new.append(Object)
                    #     if flag == False:
                    #         O_new.append("")
                    # else:
                    O_new.append(Object)
                # print(O_dict)
                # print(O_new)

                for sub in S_new:
                    for i in range(0,len(O_new)):
                        obj = O_new[i]
                        relationWord = V_new[i]
                        if obj != "":
                            # print(RawSentence)
                            # print((sub, relationWord, obj))
                            all_result.append([sub,relationWord,obj])
                            raw_sentence.append(RawSentence)

        return all_result,raw_sentence

    def hasEntity(self,word,allEntity):
        for entity in allEntity:
            if entity in word:
                # print(entity)
                return True
        return False

    def PostProcessSPO(self,rawSentence,allTripes,allEntity):
        output_list = []
        for i in range(0,len(allTripes)):
            tripe = allTripes[i]
            sub = tripe[0]
            obj = tripe[2]
            # print(sub)
            # print(obj)
            if self.hasEntity(sub,allEntity) and self.hasEntity(obj,allEntity):
                output_list.append(tripe)
        return output_list



"""
考虑到一句话越长，则LTP的效果越不好
"""
if __name__ == '__main__':
    dsfn = DSFN()

    # 分词测试
    print('***' + '分词测试' + '***')
    allSentence = []

    f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\' + "5A_天坛公园.txt"
             , 'r', encoding='utf-8')
    file = f.read()
    #    print(file)
    json_file = json.loads(file)  # 转化为json格式
    text = json_file.get("text")  # 读取text
    sentence_list = dsfn.splitSentence(text)  # 将text分为句子列表
    # print(sentence_list)

    f = open('..\\..\\entity_verb\\entity_verb_result\\' + "all_entity.json"
             , 'r', encoding='utf-8')
    file = f.read()
    all_entity = json.loads(file)['all_entity']
    new_sentence = []
    sentence_list = ["巴塞罗那的本土球员伊涅斯塔和梅西"]
    count = 0
    allTripesForGraph = []
    noBlankInSentence = []
    tripesDSFNUser = dsfn.dsfnStart(sentence_list[0], dsfn.segmentor_user, "巴塞罗那", "伊涅斯塔",
                                    all_entity)
    print(tripesDSFNUser)
    tripesDSFNUser = dsfn.dsfnStart(sentence_list[0], dsfn.segmentor_user, "巴塞罗那", "梅西",
                                    all_entity)
    print(tripesDSFNUser)
    # tripesDSFNNo = dsfn.dsfnStart(sentence_list[0], dsfn.segmentor, all_entity[index1], all_entity[index2],
    #                               all_entity)


    dsfn.close()