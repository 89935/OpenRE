import json
file = open("knowledge_triple_颐和园.json", 'r', encoding='utf-8')
knowledge_list = []
for line in file.readlines():
    dic = json.loads(line)
    knowledge_list.append(dic['知识'])
file.close()
knowledge_classification = dict()

for knowledge in knowledge_list:
    relation = knowledge[1]
#     subject = knowledge[0]
#     _location = subject.find('_')
#     subject_pos = subject[_location+1:]
    if relation not in knowledge_classification.keys():
        knowledge_classification[relation] = [tuple(knowledge)]
    else:
        knowledge_classification[relation].append(tuple(knowledge))
#     print(knowledge)
#     print(_location)
#     print(subject_pos)
# print(knowledge_classification.keys())

classification_num = dict()
for i in knowledge_classification:
    classification_num[i] = len(knowledge_classification[i])
classification_num=sorted(classification_num.items(), key=lambda item:item[1], reverse=True)
with open("result\\relation_classification_result.json", 'a') as f_out:
    try:
        # f_out.write(json.dumps(classification_num, ensure_ascii=False))
        for i in classification_num:
            f_out.write(str(i) + " : ")
            f_out.write(json.dumps(knowledge_classification[i[0]], ensure_ascii=False))
            f_out.write("\n")
    except Exception as e:
        raise
    finally:
        f_out.close()