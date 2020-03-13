import csv
import json
import thulac
thu1 = thulac.thulac()
sFileName='entity_verb_result//intersection_only_verb4.csv'

f =open('entity_verb_result\\' + "all_entity.json"
                 , 'r', encoding='utf-8')
file = f.read()
all_entity = json.loads(file)['all_entity']
verb_dict = dict()
f1 = open('entity_verb_result/verb_frequence_len2_thulac_v2.json','w',encoding='utf-8')
with open(sFileName,newline='',encoding='UTF-8') as csvfile:
    rows=csv.reader(csvfile)
    for row in rows:
        for relation in row:
            location = 0
            if len(relation)>2:
                while location < len(relation):
                    location = relation.find('_v',location)
                    end = location
                    if location==-1:
                        break
                    while relation[location]!='\'':
                        location-=1
                    verb = relation[location+1:end]
                    if verb not in verb_dict:
                        verb_dict[verb] = 1
                    else:
                        verb_dict[verb] += 1
                    location=end+2
print(verb_dict)
verb_dict = sorted(verb_dict.items(), key=lambda item: item[1], reverse=True)
new_dict = dict()
count = 0
for sort_verb in verb_dict:
    print(sort_verb)
    word = sort_verb[0]
    if len(sort_verb[0])>=2 and "=" not in sort_verb[0]:
        if  len(thu1.cut(word)) ==1 and thu1.cut(word)[0][1] != 'v':
            count+=1
            continue
        elif len(thu1.cut(word))>1:
            flag = False
            for word_pos in thu1.cut(word):
                if word_pos[1] == 'v':
                    flag = True
            if flag==False:
                count += 1
                continue
        new_dict[sort_verb[0]] = sort_verb[1]
print(new_dict)
print(len(new_dict))
print(count)
f1.write(json.dumps(new_dict,ensure_ascii=False))
# print(verb_dict)
#         print(line)
#         print("-------------------")
#         f1.write(str(line)+'\n')
f1.close()
# print(all_line)
