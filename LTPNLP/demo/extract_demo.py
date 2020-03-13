# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:33:34 2020

@author: thinkpad
"""

import os
import re
import sys
sys.path.append("..") #先跳出当前目录
from LTPNLP.core.nlp import NLP
from LTPNLP.core.extractor import Extractor

if __name__=='__main__':

    
    #实例化NLP（分词，词性标注，命名实体识别，依存句法分析）
    nlp = NLP()
    sentence_list = [
        # "北京故宫博物院建立于1925年10月10日，位于北京故宫紫禁城内",
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
                     # "珍宝馆、石鼓馆和戏曲馆这三个常设展馆位于宁寿宫区内",
                     # "天府永藏展：设在保和殿西庑房及西北崇楼，位于外朝前三殿区西侧，展示历代皇家收藏传统与清宫收藏类别",
                     # "清宫卤簿仪仗展：设在太和门西庑房，位于太和门广场西侧，展示清宫卤簿和仪仗用具",
                     # "斋宫：位于内廷后三宫区以东、东六宫区以南"
                     ]
    #遍历每一篇文档中的句子
    for origin_sentence in sentence_list:

        origin_sentence = ''.join(origin_sentence.split())
        origin_sentence=origin_sentence.strip()
        #原始句子长度小于6，跳过
        if(len(origin_sentence)<6):
            continue
        print('****')
        print(origin_sentence)
        #分词处理
        lemmas = nlp.segment(origin_sentence)
        #词性标注
        words_postag = nlp.postag(lemmas)
        #命名实体识别
        words_netag = nlp.netag(words_postag)
        #依存句法分析
        sentence = nlp.parse(words_netag)
        print(sentence.to_string())

        # extractor = Extractor()
        # num = extractor.extract(origin_sentence,sentence,output_path,num,nlp)
    nlp.close()