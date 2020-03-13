import json

def getNumOfEntityPairAndRel(fileName):
    allRel = []
    f = open(fileName, 'r', encoding='utf-8')
    file = f.read()
    f.close()
    loc_loc_triples = json.loads(file)
    countEntityPair = 0
    countCandidateRel = 0
    for entity in loc_loc_triples:
        # print(loc_loc_triples[entity])
        for entityPair in loc_loc_triples[entity]:
            countEntityPair += 1
            # print("countEntityPair:"+str(countEntityPair))
            # print(entityPair)
            # entityPair = eval(entityPair[2])
            for triples in entityPair[2]:
                allRel.append(triples[0])
                countCandidateRel += 1
                # print(triples)
                # print("countCandidateRel:"+str(countCandidateRel))
    print(allRel)
    print("countEntityPair:" + str(countEntityPair))
    print("countCandidateRel:"+str(countCandidateRel))
    return allRel

def getNumOfEntityPairAndRelAndVerb(fileName,verb):
    allRel = []
    f = open(fileName, 'r', encoding='utf-8')
    file = f.read()
    f.close()
    verbFreq = 0
    loc_loc_triples = json.loads(file)
    countEntityPair = 0
    countCandidateRel = 0
    for entity in loc_loc_triples:
        # print(loc_loc_triples[entity])
        for entityPair in loc_loc_triples[entity]:
            countEntityPair += 1
            # print("countEntityPair:"+str(countEntityPair))
            # print(entityPair)
            # entityPair = eval(entityPair[2])
            for triples in entityPair[2]:
                allRel.append(triples[0])
                countCandidateRel += 1
                if triples[0] == verb:
                    verbFreq +=1
                # print(triples)
                # print("countCandidateRel:"+str(countCandidateRel))
    print(allRel)
    print(verb+"verbFreq: "+str(verbFreq))
    print("countEntityPair:" + str(countEntityPair))
    print("countCandidateRel:"+str(countCandidateRel))
    print(verbFreq/countCandidateRel)
    return allRel

# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','位于')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','设')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','称')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','参观')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','坐落')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','成立')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','仿')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','成')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','建造')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','连接')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','称为')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','建设')
# allRel1 = getNumOfEntityPairAndRelAndVerb('document-level-output/loc_loc_triples8.json','存')


# allRel = []
# for rel in allRel1:
#     allRel.append(rel)
#
# print(set(allRel))
# print(len(set(allRel)))


allRel1 = getNumOfEntityPairAndRel('document-level-output/loc_loc_triples9.json')
allRel2 = getNumOfEntityPairAndRel('document-level-output/loc_per_triples9.json')
allRel3 = getNumOfEntityPairAndRel('document-level-output/per_loc_triples9.json')
allRel4 = getNumOfEntityPairAndRel('document-level-output/per_per_triples9.json')

# allRel1 = getNumOfEntityPairAndRel('document-level-output/windowWord1_longestEntity_(loc-loc)+(loc-per)+(per-loc)+(per-per)+/filtered-loc_loc_triples8.json')
# allRel2 = getNumOfEntityPairAndRel('document-level-output\windowWord1_longestEntity_(loc-loc)+(loc-per)+(per-loc)+(per-per)+/filtered-loc_per_triples8.json')
# allRel3 = getNumOfEntityPairAndRel('document-level-output\windowWord1_longestEntity_(loc-loc)+(loc-per)+(per-loc)+(per-per)+/filtered-per_loc_triples8.json')
# allRel4 = getNumOfEntityPairAndRel('document-level-output\windowWord1_longestEntity_(loc-loc)+(loc-per)+(per-loc)+(per-per)+/filtered-per_per_triples8.json')
# print(allRel1)
#
allRel = []
for rel in allRel1:
    allRel.append(rel)

print(set(allRel))
print(len(set(allRel)))
allRel = []
for rel in allRel2:
    allRel.append(rel)

print(set(allRel))
print(len(set(allRel)))

allRel = []
for rel in allRel3:
    allRel.append(rel)

print(set(allRel))
print(len(set(allRel)))
#
allRel = []
for rel in allRel4:
    allRel.append(rel)

print(set(allRel))
print(len(set(allRel)))

allRel = []
for rel in allRel1:
    allRel.append(rel)
for rel in allRel2:
    allRel.append(rel)
for rel in allRel3:
    allRel.append(rel)
for rel in allRel4:
    allRel.append(rel)
print(allRel)
print(set(allRel))
print(len(set(allRel)))
# getNumOfEntityPairAndRel('document-level-output\\1(loc-loc)+(loc-per)+(per-per)+\\filtered-per_per_triples2.json')
















# f = open('document-level-output\\loc_loc_triples.json', 'r', encoding='utf-8')
# file = f.read()
# f.close()
# print(file)
# print(len(file))
# f = open('document-level-output\\loc_per_triples.json', 'r', encoding='utf-8')
# file = f.read()
# f.close()
# print(file)
# print(len(file))
# f = open('document-level-output\\loc_per_triples2.json', 'r', encoding='utf-8')
# file = f.read()
# f.close()
# print(file)
# print(len(file))