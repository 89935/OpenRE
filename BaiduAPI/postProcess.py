# -*- coding: utf-8 -*-
simDict = dict()
for line in open("sim.txt","r", encoding='utf-8'):  # 设置文件对象并读取每一行文件
    if ":" in line:
        text_list = line.split(":")
        if "None" not in text_list[1] and "illegal multibyte sequence" not in text_list[1]:
            simDict[text_list[0]] = text_list[1].strip("\n")
# print(simDict)
simDict = sorted(simDict.items(), key=lambda item: item[1],reverse=True)
print(simDict)
with open('sortedSim.txt', 'w',encoding='utf-8') as file:
    for dict1 in simDict:
        file.write(str(dict1))
        file.write("\n")