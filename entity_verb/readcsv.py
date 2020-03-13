import csv
import json
sFileName='entity_verb_result//intersection_only_verb_windowWord_1_beforeAndAfter.csv'

f =open('entity_verb_result\\' + "all_entity.json"
                 , 'r', encoding='utf-8')
file = f.read()
all_entity = json.loads(file)['all_entity']

f1 = open('entity_verb_result/simple_relation_v6_one_sentence_beforeAndAfter.txt','w',encoding='utf-8')
with open(sFileName,newline='',encoding='UTF-8') as csvfile:

    rows=csv.reader(csvfile)

    all_entity = []
    for row in rows:
        print(row)
        all_entity = row
        break
    count = 0
    num = 0
    for row in rows:
        line = []
        count = count+1
        print(row)
        """
        有顺序、带有（自己，自己）实体对
        """
        # for i in range(1,len(all_entity)):
        #     num = num + 1
        #     if len(row[i])>2:
        #         line.append(row[0]+'---'+all_entity[i]+" : "+row[i])
        """
        有顺序、不带有（自己，自己）实体对
        """
        for i in range(1, len(all_entity)):
            num = num + 1
            if row[0]!=all_entity[i] and len(row[i]) > 2:
                line.append(row[0] + '---' + all_entity[i] + " : " + row[i])
        """
        无顺序、带有（自己，自己）实体对
        """
        # for i in range(1,count+1):
        #     num = num + 1
        #     if len(row[i])>2:
        #         line.append(row[0]+'---'+all_entity[i]+" : "+row[i])

        """
        无顺序、且不带有（自己，自己）实体对
        """
        # for i in range(1,count):
        #     num = num + 1
        #     if len(row[i]) > 2:
        #         line.append(row[0] + '---' + all_entity[i] + " : " + row[i])
        # print(line)
        # print(num)
        print("-------------------")
        f1.write(str(line)+'\n')
        # break
    print(count)
    print(num)
# f1.close()
# print(all_line)
