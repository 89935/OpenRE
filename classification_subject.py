import json
file = open("knowledge_triple_颐和园.json", 'r', encoding='utf-8')
knowledge_list = []
for line in file.readlines():
    dic = json.loads(line)
    knowledge_list.append(dic['知识'])
file.close()
knowledge_classification = dict()

for knowledge in knowledge_list:
    subject = knowledge[0]
    _location = subject.find('_')
    subject_pos = subject[_location+1:]
    if subject_pos not in knowledge_classification.keys():
        knowledge_classification[subject_pos] = [tuple(knowledge)]
    else:
        knowledge_classification[subject_pos].append(tuple(knowledge))
    print(knowledge)
    print(_location)
    print(subject_pos)
print(knowledge_classification.keys())

with open("result\\subject_classification_result.json", 'a') as f_out:
    try:
        f_out.write(json.dumps(knowledge_classification,ensure_ascii=False))
        for i in knowledge_classification:
            f_out.write("\n"+i+" : ")
            f_out.write(str(len(knowledge_classification[i])))


        f_out.write('\n')
        f_out.flush()
    except Exception as e:
        raise
    finally:
        f_out.close()