import json
f = open("D:\python-file\北京市旅游知识图谱\\"
         , 'r', encoding='utf-8')
# file = f.read()
# json_file = json.loads(file)
for line in f.readlines():
    json_line = json.loads(line)
    print(json_line)