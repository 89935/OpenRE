# coding=gbk
import json
import re


def splitSentence(text):
    pattern = r'��|��|��|��|='
    result_list = re.split(pattern, text)
    result_list = list(filter(not_empty, result_list))
    #    print(result_list)
    return result_list

def not_empty(s):
        return s and "".join(s.split())

def occurrence(sentence_list, entity1, entity2):
    result_list = []
    for sentence in sentence_list:
        if entity1 in sentence and entity2 in sentence:
            result_list.append(sentence)
    return result_list


if __name__ == "__main__":
    place = []
    fileList = ['5A_�ú�԰.txt','5A_�����ʹ�����Ժ.txt','5A_�ú�԰.txt','5A_Ľ��������.txt','5A_��̳��԰.txt']
    for fileName in fileList:
        f = open('D:\python-file\����������֪ʶͼ��\\verb-entity\\bj_travel\\' + fileName
                 , 'r', encoding='utf-8')
        file = f.read()
        #    print(file)
        json_file = json.loads(file)  # ת��Ϊjson��ʽ
        text = json_file.get("text")  # ��ȡtext

        sentence_list = splitSentence(text)  # ��text��Ϊ�����б�

        # print(sentence_list)
        # print(len(sentence_list))
        # entity1 = "Ǭ�幬"
        # entity2 = "λ��"
        entity1 = "λ��"
        entity2 = "λ��"
        resultList = occurrence(sentence_list, entity1, entity2)
        for result in resultList:
            print(result)
    # outputDict = dict()
    # person=["������", "���", "¬����", "����", "��¥��", "�̾���", "������", "����", "���", "�쾮", "�ƹ���", "�ܶ���", "������", "����", "����", "����", "����", "���", "����", "�������", "����", "�ط�", "������", "���Ļ�", "������", "����", "Ѧ����", "ի��", "���", "��ΰ", "����", "��ȫ", "����", "����", "�׶�԰", "���»�", "��ï", "�󶼻�", "����", "Ԫ", "ˮī", "��ά��", "����", "����������", "�۹�����", "������", "���㹬", "����", "��������", "õ��", "�����", "��ѧ��", "�˰�", "����", "����", "̫������", "��ѷ", "ʯʨ", "�Ʊ�", "����", "�����", "���", "¿��", "��", "ս��", "���������", "����ӳ", "����", "����", "����", "������", "����", "����", "¡��", "��ҵ��", "����", "���ؾ�", "��٥", "Ӻ��", "����", "��ڷ", "���ٳ�", "��Ԫ��", "����", "�ܵ���", "����", "������", "��Դ�", "���Ļ�", "�¾�˼", "����", "����", "������", "��Դ", "������", "������", "��¬ñ", "����", "̫��", "̤��", "����", "�޼һ�", "�Բ��X", "���ʷ�", "����֮", "½��", "����", "����", "����", "�峯", "����", "����", "����͢", "����", "����֮", "�ż�", "¹����", "�ӱ�", "�λ�����٥", "�ż�֮", "Тʥ�ܻʺ�", "���", "�캣", "������", "����", "��Ԩ", "��ͳ", "���", "����", "�", "�챦ʯ", "���", "����", "�ݼ̹�", "ͳ����", "����", "�´�", "ŷ����", "ʯ��", "�����ʹ�", "��ѩ", "��������", "��˵", "���", "������", "����³", "��������", "������", "ս��Ʒ", "���ݰ˹�", "����ԭ", "����", "�ܲ���", "���", "����", "��ʯ", "��Է", "����Ĥ��", "����", "��ԫ", "����", "��ׯ", "��ͥ��", "����", "���", "����", "�ｭ", "����", "Ӣ��", "������", "��ɽ", "ѷ��", "�ɻ�", "��Ȫ", "����", "�Ʒ�", "����", "����j�j", "�ۺ�", "����", "��֮�[", "��Դ", "������", "������", "�Ƴ�", "��", "����ʯ", "������", "���ľ�", "����ά", "���", "����", "����", "����", "�Բ���", "����", "����", "����", "���͹�", "������", "�����ٷ�", "����", "ת�ֲ�", "��԰", "����", "����", "������", "����", "����", "�����", "���b", "����", "÷չ", "Т�Ǵ��ʺ�", "�ķ�֮��", "����", "����", "����", "����", "�ջ�", "������ҹ��ͼ", "�����", "���Ĵ�ؾ�", "����", "Ǯѡ", "��Ԫ�", "����", "̩ɽ", "������������ѧԺ", "���ɽ", "����", "���", "������", "���µ�һ", "������", "�ɻ�", "�ܕP", "����", "�ʺ�", "����", "ʯ��", "�ź�", "���", "����", "������", "����", "��Ӣ", "ʮ�߿���", "��ĭ��", "��ʽ��", "����", "������", "�Բ�", "Ф��", "����", "����", "����", "����", "����", "���", "����", "������", "��", "����", "���", "����", "�Ĳ��۾�", "����", "����", "��ϣ��", "��Ժ", "�����", "��ɽ", "����԰", "����", "���", "����̫��", "����", "������", "�Ű�", "����", "ϲ��", "����", "�Ĵ���", "�׽�", "�ŵ�԰��", "��������", "����", "ʯ��", "�ʼ���", "����", "�⻨", "�����Ĺ־��", "�й��ŵ�԰��", "�ȶ����Ǵ�", "����", "����", "����", "����Ӣ", "������", "�ķ��ı�", "���", "��μ", "�̻�ѧУ", "÷��", "���", "������", "��ѵ", "����", "����֮", "����", "�����", "��ͼ³", "����ʽ", "��ϣ��", "����", "Ѧ����", "���ķ���ȫ�ؾ�", "��ǰ����", "��ë", "Ӣ��", "�ϴ�", "��̴", "�����\", "��Ӻ", "����ʵ�", "��̨", "�Ʋ���", "�ɽ�", "����", "��Ʒ", "�־���", "�����", "�Ϸ�", "����", "����", "��ҹ��", "�����", "ĩ��", "������", "���", "�鷶", "��۬", "��ѩ", "����֮", "չ���", "ɽ��ͼ", "�γ���", "����", "����", "�ش����", "ŷ��ѯ", "������", "���岩", "�����", "��ֱ", "�ڽ̽���", "�辰", "���ϼ�", "����", "���¾��ޡ�����", "���", "����", "÷��", "����", "���Ϲ�", "�Ͼ�", "�����", "���ĵ�", "���", "�", "����", "������", "Ъɽ��", "��ۮ", "����", "����ի", "����", "����", "�ƺ�¥", "���Ӽ�", "����", "�ײ�", "����", "��ʯ", "������", "��", "����", "��չ", "��ʿڱ", "����", "����", "�ް�", "����", "�����", "�Űٷ�", "��ʥ��", "����", "�¾���", "����", "����", "����", "Τ��", "���Ĳ���", "����", "Muse", "������", "����", "��Ů", "�Ĺ�", "��ʦ��", "ë��", "����", "���͵�", "�ĳ�԰", "�л�����", "���", "��ͳ", "�·�", "������", "����", "�Ĳ���", "����Ī��", "�º��", "������", "������", "����", "������", "����", "ĵ��", "���޾�", "����", "����", "����", "���Ĵ�ؾ�", "���", "�ű���̫��", "½��", "κ����", "��ľ", "����", "����", "½��", "������", "�����", "ʷ��", "������", "����", "����", "ɨ��", "�ʵ�", "��Զ", "�߿˹�", "ɽ�ж�����", "��ʳ�Ļ�", "����", "����", "������", "����", "�����ʻ�", "�����", "����", "����", "����", "����", "�ĺ�Ժ", "�����Ϻ�ͼ", "����", "����", "����", "ʢ��", "����", "���", "����֮", "��֪��", "Ǭ¡", "����", "��΢ԫ", "����"]
    # for index1 in range(0,len(person)):
    #     for index2 in range(index1+1,len(person)):
    #         print( person[index1] + "--" +  person[index2])
    #         sentenceIncluding_list = occurrence(sentence_list, person[index1], person[index2])
    #         if len(sentenceIncluding_list) != 0:
    #             outputDict[str(index1)+"--"+str(index2)] = sentenceIncluding_list
    # with open('entity_verb_result\\' + "PersonOccurrenceSentence.json", 'w',
    #           encoding='utf-8') as json_file:
    #     json_file.write(json.dumps(outputDict, ensure_ascii=False))
    # print(len(sentenceIncluding_list))
    # for sentenceIncluding in sentenceIncluding_list:
    #     print(sentenceIncluding)