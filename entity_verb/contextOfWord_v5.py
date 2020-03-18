"""
修改内容：缩小上下文范围，只考虑一句话中前一个动词和后一个动词，EVList利用的是
"""
import json

import os
from pyltp import Segmentor,SentenceSplitter,Postagger,NamedEntityRecognizer,Parser
import thulac
from entity_verb.nlp import NLP
from entity_verb.entity_verb_new import entity_verb_new
import os
def remove_(text):
    text = text.replace("===","=")
    text = "".join(text.split())
    return text


def contextOfEntity(text_clean, entity, window_size):
    result_list = []
    print(text_clean)
    index = 0
    while index<len(text_clean):
        index = text_clean.find(entity,index)
        if index==-1:
            break
        else:
            result_list.append(text_clean[index-window_size:index+window_size+len(entity)])
            index += len(entity)
    return result_list

def TopEntityAndVerb(result_list2):
    entityDictAll = dict()
    entityDictOnlyVerb = dict()
    for EV_list in result_list2:
        for EV in EV_list:
            word = EV[0]
            numLocation = word.find("#")
            _location = word.find("_")
            if numLocation != -1:
                word = word[numLocation + 1:]
            else:
                word = word
            if word not in entityDictAll.keys():
                entityDictAll[word] = 1
            else:
                entityDictAll[word] += 1
            if "v" in word:
                if word not in entityDictOnlyVerb.keys():
                    entityDictOnlyVerb[word] = 1
                else:
                    entityDictOnlyVerb[word] += 1
    entityDictAll = sorted(entityDictAll.items(), key=lambda item: item[1], reverse=True)
    entityDictOnlyVerb = sorted(entityDictOnlyVerb.items(), key=lambda item: item[1], reverse=True)
    return entityDictAll,entityDictOnlyVerb

def not_empty(s):
    return s and "".join(s.split())


def stopwordsList():
    """
    return:停用词列表
    """
    stop_list_Path = 'source\\中文停用词.txt'
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

def findEntityLocation(entity,wordList):

    startLoc = -1
    finishLoc = -1
    for i in range(len(wordList)):
        word = ""
        if (startLoc==-1 or finishLoc==-1) and wordList[i] in entity: #
            word += wordList[i]
            startLoc = i
            # print("GOGOGO"+str(startLoc))
            for j in range(i+1,len(wordList)):
                if word + wordList[j] in entity:
                    word += wordList[j]
                else:
                    if word==entity:
                        finishLoc = j-1
                    else:
                        startLoc = -1
                        finishLoc = -1
                        break
                if startLoc!=-1 and finishLoc!=-1:
                    break
    return startLoc,finishLoc

def EVoccurrence(text,entity1):
    EVListHasEntity = []
    for EVList in text:
        flag1 = False
        for item in EVList:
            word = item[0]
            location = word.find("_")
            Numlocation = word.find("#")
            word = word[Numlocation+1:location]
            # print(item)
            # print(word)
            if flag1==False:
                if entity1 == word:
                    flag1 = True
            if flag1 == True:
                EVListHasEntity.append(EVList)
                break
    return EVListHasEntity


def getCompanyVerbInaSentence(entity,num,result_list,maxDistance):
    """

    :param entity: 实体名称
    :param num: 前后各num个动词
    :param result_list: 含有该entity的EVList
    :param maxDistance: 该实体距离动词的最大距离
    :return: 该实体一个伴随动词集合
    """
    verb_freq_dict = dict()
    for EV in result_list:
        print(EV)
        count = -1
        for item in EV:
            count +=1
            word = item[0]
            location = word.find("_")
            Numlocation = word.find("#")
            word = word[Numlocation + 1:location]
            if Numlocation!=-1 and word == entity:  # 只有NumLocation！=-1才是实体,==-1是一个动词
                verbNum = 0
                for i in range(count-1,-1,-1):
                    # print(EV[i])
                    verb = EV[i][0]
                    location = verb.find("_")
                    Numlocation = verb.find("#")
                    verb = verb[Numlocation + 1:location] + '_before'  # 动词在实体前
                    if 'v' in EV[i][0] and Numlocation == -1:  # 通过NumLocation来确保是个动词，而不是一个实体，考虑实体“收藏”
                        if (item[1] - (EV[i][1]+len(verb.split('_')[0])))>maxDistance:
                            print(item[1] - (EV[i][1] + len(verb.split('_')[0])))
                            break
                        verbNum += 1
                        print(verb)
                        if verb not in verb_freq_dict:
                            verb_freq_dict[verb] = 1
                        else:
                            verb_freq_dict[verb] +=1
                        if verbNum == num:
                            break

                verbNum = 0
                for i in range(count + 1, len(EV)):
                    # print(EV[i])
                    verb = EV[i][0]
                    location = verb.find("_")
                    Numlocation = verb.find("#")
                    verb = verb[Numlocation + 1:location] + '_after'  # 动词在实体后
                    if 'v' in EV[i][0] and Numlocation == -1:  # 通过NumLocation来确保是个动词，而不是一个实体，考虑实体“收藏_v”
                    # if 'v' in EV[i][0] :  # 只要该单词被识别为动词即可，不用管是不是实体，因为有些实体仍然可以作为动词关系
                        if (EV[i][1]- ( item[1]+len(word)))>maxDistance:
                            print((EV[i][1]) - ( item[1]+len(word)))
                            break
                        verbNum += 1
                        print(verb)
                        if verb not in verb_freq_dict:
                            verb_freq_dict[verb] = 1
                        else:
                            verb_freq_dict[verb] += 1
                        if verbNum == num:
                            break
    verb_freq_dict = sorted(verb_freq_dict.items(), key=lambda item: item[1], reverse=True)
    print(verb_freq_dict)
    return verb_freq_dict


if __name__ == "__main__":

    """
    加载LTP的分词器和词性标注器
    """
    default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\'  # LTP模型文件目录
    segmentor = Segmentor()
    user_dict = "source\\user.txt"
    segmentor_flag = segmentor.load_with_lexicon(os.path.join(default_model_dir, 'cws.model'), user_dict)

    postagger = Postagger()
    postag_flag = postagger.load(os.path.join(default_model_dir, 'pos.model'))

    # fileList = ['5A_北京故宫博物院.json', '5A_天坛公园.json','5A_恭王府.json','5A_颐和园.json','5A_慕田峪长城.json']
    fileList = ['all_只包含最长实体2.json']
    json_file = []
    for file_name in fileList:
        print(file_name)
        f = open('entity_verb_result\\ltp-ltp去除停用词\\' + file_name, 'r', encoding='utf-8')
        for line in f.readlines():
            json_line = json.loads(line)
            for key in json_line:
                json_file.append(json_line.get(key))
    print(json_file)
    f = open('entity_verb_result\\' + "all_entity.json"
             , 'r', encoding='utf-8')
    file = f.read()
    all_entity = json.loads(file)['all_entity']
    f.close()

    all_entity = ["大角楼","什刹海"]
    word_freq_dict = dict()
    for entity in all_entity:
        EVList = EVoccurrence(json_file, entity)  # 获取该实体的EVList
        print(EVList)
        verbFrequenceDict = getCompanyVerbInaSentence(entity, 1, EVList,10)  # 获取该实体在EVList前后各一个动词，以及词频；
        # 10 代表该实体与第一个动词最大距离，感觉有点大

        word_freq_dict[entity] = verbFrequenceDict
    print(word_freq_dict)



        # print(text_clean)

    # window_size = 10
    # entity_context_dict = dict()
    # word_freq_dict = dict()
    #
    # all_entity = ["颐和园"]
    # for entity in all_entity:
    #     result_list = contextOfEntity(all_documents, entity, window_size)  # 获得该实体window-size窗口大小的上下文
    #     print(result_list)
    #     EV_list = EVListOfContext(entity,1,result_list,segmentor,postagger)
    #
    #     word_freq_dict[entity] = EV_list
    # print(word_freq_dict)


    # with open('entity_verb_result\\' + "context_word_freq_dict_v6_longestEntity__one_sentence_beforeAndAfter2.json", 'w',
    #           encoding='utf-8') as json_file:
    #     json_file.write(json.dumps(word_freq_dict,ensure_ascii=False))


    # print(entity_context_dict)
    # with open('entity_verb_result\\' + "all_entity_context.json", 'w',
    #           encoding='utf-8') as json_file:
    #     json_file.write(json.dumps(entity_context_dict,ensure_ascii=False))
    # f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\' + "5A_北京故宫博物院.txt"
    #          , 'r', encoding='utf-8')
    # file = f.read()
    # #    print(file)
    # json_file = json.loads(file)  # 转化为json格式
    # text = json_file.get("text")  # 读取text
    # print(text)
    # text_clean = remove_(text)
    # print(text_clean)
    # entity1 = "乾隆"
    # entity2 = "故宫"
    # window_size = 10
    # result_list = contextOfEntity(text_clean, entity1, window_size)
    # print(result_list)
    # result_list2 = contextOfEntity(text_clean, entity2, window_size)
    # entity_verb_new = entity_verb_new()
    # all_entity = entity_verb_new.readAllEntity()
    # nlp = NLP()
    # thu1 = thulac.thulac()
    # EV_list=entity_verb_new.mapEntity(result_list, all_entity, thu1, nlp)
    # EV_list2=entity_verb_new.mapEntity(result_list2, all_entity, thu1, nlp)
    # entityDictAll,entityDictOnlyVerb = TopEntityAndVerb(EV_list)
    # entityDictAll2,entityDictOnlyVerb2 = TopEntityAndVerb(EV_list2)
    # print(entityDictAll)
    # print(entityDictOnlyVerb)
    # print(entityDictAll2)
    # print(entityDictOnlyVerb2)
    # for i in range(len(result_list2)):
    #     print(result_list2[i])
    #     print(EV_list2[i])
