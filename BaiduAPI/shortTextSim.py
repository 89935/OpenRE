# -*- coding: utf-8 -*-
from aip import AipNlp
import json

""" 你的 APPID AK SK """
APP_ID = '18594776'
API_KEY = '3R7LnRGRf2mqAvw4KxGGjEkK'
SECRET_KEY = '0lFUjawAmYqH2LMiNmpuOq6faIgKR6bI'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# text1 = "谷牧同志"
#
# text2 = "谷牧领导同志"

# text1 = "厉善麟祖父厉子嘉"
#
# text2 = "厉子嘉"

# text1 = "恭亲王"
#
# text2 = "恭亲王奕忻"

# f = open("..//LTPNLP//core//outputTripes//带所有修饰的结果.json","r", encoding='utf-8')
# file = f.read()
# all_triples = json.loads(file)['result']
# subject_list = []
# for triple in all_triples:
#     subject_list.append(triple[0])
# subject_set = set(subject_list)
# subject_list = []
# simDict = dict()
# for subject1 in subject_set:
#     subject_list.append(subject1)
# for index1 in range(len(subject_list)):
#     for index2 in range(index1+1,len(subject_list)):
#         text1 = subject_list[index1]
#         text2 = subject_list[index2]
#         try:
#             score = client.simnet(text1, text2).get("score")
#         except Exception as e:
#             print(text1+""+text2)
#             print(e)
#
#         simDict[text1+""+text2] = score
#         print(text1+"+"+text2+":"+str(score))
# simDict = sorted(simDict.items(), key=lambda item: item[1])
# print(simDict)
# with open('output\\' + "相似性结果.json", 'w',
#           encoding='utf-8') as json_file:
#     json_file.write(json.dumps(simDict, ensure_ascii=False))
# +
""" 调用短文本相似度 """
# client.simnet(text1, text2);
# print(client.simnet(text1, text2).get("score"));
""" 调用词义相似度 """
print(client.simnet("奥巴马", "奥巴马先生"))
