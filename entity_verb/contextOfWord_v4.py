"""
修改内容：取实体周围的i个动词，且表明该动词是在实体前还是实体后
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
    # print(text_clean)
    index = 0
    while index<len(text_clean):
        index = text_clean.find(entity,index)
        if index==-1:
            break
        else:
            result_list.append(text_clean[index-window_size:index+window_size+len(entity)])
            index += len(entity)
    return result_list

def stopwordsList():
    """
    return:停用词列表
    """
    stop_list_Path = 'source\\中文停用词.txt'
    f = open(stop_list_Path, 'r', encoding='utf-8')
    stopwords = [line.strip() for line in f.readlines()]
    #    print(stopwords)
    return stopwords

def EVListOfContext(entity,num,result_list,segmentor,postagger,window_size):
    """
    取离实体最近的前后各num个动词
    :param entity: 实体
    :param num: 前后各取几个动词
    :param result_list: 上下文列表
    :param segmentor:
    :param postagger:
    :param window_size: 上下文的窗口大小
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
        print("1:"+str(result_words))  # 输出分词结果
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
        print("2:"+str(word_pos_list))  # 输出词性标注结果
        for i in range(len(result_words_num)):
            word_pos_list_num.append(tuple([result_words_num[i],pos[i]]))
        # print(word_pos_list_num)

        count = 0
        # for i in range(window_size-1,-1,-1):  # 从第9个字开始，直到第0个
        i = window_size-1
        while i >=0:
            # print(i)
            flag = False
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

                    # print(word)
                    """
                    before代表该动词在实体之前
                    """
                    if word not in stopwords and len(word.strip()) != 0:
                        print(word+'_before')
                        if word + '_before' not in word_pos_freq_dict:
                            # print(word_pos)
                            word_pos_freq_dict[word + '_before' ] = 1
                        else:
                            # print(word_pos_freq_dict)
                            word_pos_freq_dict[word + '_before'] = word_pos_freq_dict[word + '_before'] + 1
                    if flag == False:
                        i = i - len(word)
                        flag = True
                        break
            if flag == False:
                i = i - 1

        count = 0
        # for i in range(window_size+len(entity),2*window_size+len(entity)):  # 最后10个字
        i = window_size + len(entity)

        while i < 2*window_size+len(entity):
            flag = False
            # print(i)
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
                    # print(word)
                    """
                    after代表该动词在实体之后
                    """
                    if word not in stopwords and len(word.strip()) != 0:
                        print(str(count)+word+'_after')
                        if word + '_after' not in word_pos_freq_dict:
                            # print(word_pos)
                            word_pos_freq_dict[word + '_after' ] = 1
                        else:
                            # print(word_pos_freq_dict)
                            word_pos_freq_dict[word + '_after'] = word_pos_freq_dict[word + '_after'] + 1
                    if flag == False:
                        i = i + len(word)
                        flag = True
                        break
            if flag == False:
                i = i + 1

    word_pos_freq_dict = sorted(word_pos_freq_dict.items(), key=lambda item: item[1], reverse=True)
    return word_pos_freq_dict


if __name__ == "__main__":

    """
    加载LTP的分词器和词性标注器
    """
    default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\'  # 1、您需要修改一下LTP的文件目录
    segmentor = Segmentor()
    user_dict = "source\\user.txt"  # 2、您需要修改LTP的一个用户词典，我这里的用户词典就是所有的实体
    segmentor_flag = segmentor.load_with_lexicon(os.path.join(default_model_dir, 'cws.model'), user_dict)

    postagger = Postagger()
    postag_flag = postagger.load(os.path.join(default_model_dir, 'pos.model'))


    path = r"D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel"  # 3、存储所有景点文件的目录
    f = open('entity_verb_result\\' + "all_entity.json"  # 4、所有实体的文件名
             , 'r', encoding='utf-8')
    file = f.read()
    all_entity = json.loads(file)['all_entity']  # 5、所有实体json文件的key
    f.close()
    file_list = os.listdir(path)
    all_documents = ""
    for file_name in file_list:
        # print(file_name)
        f = open('D:\python-file\北京市旅游知识图谱\\verb-entity\\bj_travel\\' + file_name  # 6、替换景点文件的路径
                 , 'r', encoding='utf-8')
        file = f.read()
        #    print(file)
        json_file = json.loads(file)  # 转化为json格式
        text = json_file.get("text")  # 读取text
        text_clean = remove_(text)
        all_documents += text_clean
        f.close()
    # print(all_documents)

        # print(text_clean)

    window_size = 10  # 7、实体上下文的窗口大小，前后各window_size个字
    entity_context_dict = dict()
    word_freq_dict = dict()

    # all_entity = ["故宫"]
    for entity in all_entity:
        result_list = contextOfEntity(all_documents, entity, window_size)  # 获得该实体window-size窗口大小的上下文
        print(result_list)  # 输出该实体的上下文
        EV_list = EVListOfContext(entity,1,result_list,segmentor,postagger,window_size)  # 8、这里的1代表，我们在该实体前后各取1个动词

        word_freq_dict[entity] = EV_list

    print(word_freq_dict)  # 输出最终的结果{实体名：[(动词_after(_before)，出现的次数)]}
    with open('entity_verb_result\\' + "context_only_word_freq_dict03-16修改了循环方法.json", 'w',  # 9、最后更改输出的文件名
              encoding='utf-8') as json_file:
        json_file.write(json.dumps(word_freq_dict,ensure_ascii=False))