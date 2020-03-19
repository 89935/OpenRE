import json
f = open('sentence_level2_result\\V0.5\\loc_loc_triples.json'
                 , 'r', encoding='utf-8')
file = f.read()
#    print(file)
json_file = json.loads(file)  # 转化为json格式
# print(json_file)
f.close()
triplesList5 = []
for triple in json_file:
    str1 = triple[0] + '--' + triple[1]+'--'+triple[2]
    triplesList5.append(str1)

print(triplesList5)
print(len(triplesList5))

f = open('sentence_level2_result\\V0.4\\loc_loc_triples.json'
                 , 'r', encoding='utf-8')
file = f.read()
#    print(file)
json_file = json.loads(file)  # 转化为json格式
# print(json_file)
f.close()
triplesList4 = []
for triple in json_file:
    str1 = triple[0] + '--' + triple[1]+'--'+triple[2]
    triplesList4.append(str1)

print(triplesList4)
print(len(triplesList4))

print(set(triplesList4).difference(set(triplesList5)))
print(set(triplesList5).difference(set(triplesList4)))

