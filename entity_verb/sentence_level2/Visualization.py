import json
fileList = ["loc_loc_triples","loc_per_triples","loc_org_triples","per_loc_triples","per_per_triples","per_org_triples",
            "org_loc_triples","org_per_triples","org_org_triples","loc_time_triples","per_time_triples","org_time_triples",
            "time_loc_triples","time_per_triples","time_org_triples"]
for fileName in fileList:
    f = open('sentence_level2_result\\V0.5\\'+fileName+'.json'
                     , 'r', encoding='utf-8')
    file = f.read()
    #    print(file)
    json_file = json.loads(file)  # 转化为json格式
    # print(json_file)
    f.close()
    triplesList5 = []
    for triple in json_file:
        triplesList5.append(tuple(triple))


    with open('sentence_level2_result\\V0.5\\'+fileName+'.txt', 'a+', encoding='utf-8') as f:
        for triple in triplesList5:
            f.write(triple[0] + ',' + triple[1] + ',' + triple[2] + '\n')  # 加\n换行显示
    print(triplesList5)