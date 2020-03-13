"""
修改内容：取实体周围的i个动词
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

def EVListOfContext(entity,num,result_list,segmentor,postagger):
    """
    取离实体最近的前后各num个动词
    :param entity: 实体
    :param num: 前后各取几个动词
    :param result_list: 上下文列表
    :param segmentor:
    :param postagger:
    :return:
    """
    word_pos_freq_dict = dict()

    stopwords = stopwordsList()

    for line in result_list:
        word_pos_list = []
        words = segmentor.segment(line)
        result_words= []
        for word in words:
            # if word not in stopwords and len(word.strip()) != 0:
            if '▪' == word:
                word = '.'
            result_words.append(word)
        # print("1:"+str(result_words))
        pos = postagger.postag(result_words)
        locOfEntity = -1  # 该实体在句子中的位置，从0开始计算
        for i in range(len(result_words)):
            word_pos_list.append(tuple([result_words[i],pos[i]]))
        result_words_num = []
        count = 0
        for word in result_words:
            words_num = []
            for char in word:
                words_num.append(count)
                count+=1
            result_words_num.append(words_num)
        # print(result_words_num)
        word_pos_list_num = []
        # print("2:"+str(word_pos_list))
        for i in range(len(result_words_num)):
            word_pos_list_num.append(tuple([result_words_num[i],pos[i]]))
        # print(word_pos_list_num)

        count = 0
        for i in range(9,-1,-1):  # 从第9个字开始，直到第0个
            # if len(line)!=0:
            #     print(line[i])
            no = -1
            if count == num:  # 是否达到目标
                break
            for word_pos_num in word_pos_list_num:  # 遍历整个的Word-POS对，这里的word是用序号表示的
                no+=1  # 是第几个三元组
                if i in word_pos_num[0] and word_pos_num[1] == 'v':  # 该字是否在word里出现，且POS为V
                    count += 1
                    word = word_pos_list[no][0]

                    print(word)

                    if word not in stopwords and len(word.strip()) != 0:
                        if word + '_v' not in word_pos_freq_dict:
                            # print(word_pos)
                            word_pos_freq_dict[word + '_v' ] = 1
                        else:
                            # print(word_pos_freq_dict)
                            word_pos_freq_dict[word + '_v'] = word_pos_freq_dict[word + '_v'] + 1

        count = 0
        for i in range(10+len(entity),20+len(entity)):
            no = -1
            # if len(line)!=0:
            #     print(line[i])
            if count == num:
                break
            for word_pos_num in word_pos_list_num:
                no+=1

                if i in word_pos_num[0] and word_pos_num[1] == 'v':
                    count += 1
                    # print(word)
                    word = word_pos_list[no][0]
                    print(word)
                    if word not in stopwords and len(word.strip()) != 0:
                        if word + '_v' not in word_pos_freq_dict:
                            # print(word_pos)
                            word_pos_freq_dict[word + '_v' ] = 1
                        else:
                            # print(word_pos_freq_dict)
                            word_pos_freq_dict[word + '_v'] = word_pos_freq_dict[word + '_v'] + 1

    word_pos_freq_dict = sorted(word_pos_freq_dict.items(), key=lambda item: item[1], reverse=True)
    return word_pos_freq_dict

def onlyEListOfContext(result_list,segmentor):
    word_freq_dict = dict()

    stopwords = stopwordsList()

    for line in result_list:
        word_pos_list = []
        words = segmentor.segment(line)
        result_words= []

        for word in words:
            if word not in stopwords and len(word.strip()) != 0:
                result_words.append(word)
        for word in result_words:
            if word not in word_freq_dict.keys():
                word_freq_dict[word] = 1
            else:
                word_freq_dict[word] = word_freq_dict[word]+1

    word_freq_dict = sorted(word_freq_dict.items(), key=lambda item: item[1], reverse=True)
    # print(word_pos_freq_dict)
    return word_freq_dict

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


    path = r"D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel"
    f = open('entity_verb_result\\' + "all_entity.json"
             , 'r', encoding='utf-8')
    file = f.read()
    all_entity = json.loads(file)['all_entity']
    f.close()
    file_list = os.listdir(path)
    all_documents = ""
    for file_name in file_list:
        # print(file_name)
        f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\' + file_name
                 , 'r', encoding='utf-8')
        file = f.read()
        #    print(file)
        json_file = json.loads(file)  # 转化为json格式
        text = json_file.get("text")  # 读取text
        text_clean = remove_(text)
        all_documents += text_clean
        f.close()
    print(all_documents)

        # print(text_clean)

    window_size = 10
    entity_context_dict = dict()
    word_freq_dict = dict()

    # all_entity = ["乾隆"]
    for entity in all_entity:
        result_list = contextOfEntity(all_documents, entity, window_size)  # 获得该实体window-size窗口大小的上下文
        print(result_list)
        EV_list = EVListOfContext(entity,1,result_list,segmentor,postagger)
        # E_list = onlyEListOfContext(result_list,segmentor)
        # print(E_list)
        # print(EV_list)
        word_freq_dict[entity] = EV_list
        # entity_context_dict[entity] = result_list
    print(word_freq_dict)
    # with open('entity_verb_result\\' + "context_only_word_freq_dict.json", 'w',
    #           encoding='utf-8') as json_file:
    #     json_file.write(json.dumps(word_freq_dict,ensure_ascii=False))


    with open('entity_verb_result\\' + "context_word_freq_dict_v3.json", 'w',
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(word_freq_dict,ensure_ascii=False))
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
