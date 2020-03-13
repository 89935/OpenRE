from entity_verb.nlp import NLP
import json
f =open('entity_verb_result\\' + "all_entity.json"
                 , 'r', encoding='utf-8')
file = f.read()
all_entity = json.loads(file)['all_entity']
f.close()
nlp =NLP()
postag_dict = dict()
for word in all_entity:
    postage = nlp.get_postag(word)
    if postage not in postag_dict.keys():
        postag_dict[postage] = [word]
    else:
        postag_dict[postage].append(word)
print(postag_dict)
for i in postag_dict.keys():
    postag_dict_new  = dict()
    postag_dict_new[i+'_'+str(len(postag_dict[i]))] = list(postag_dict[i])
    with open("entity_verb_result\\entity_classification_LTP.json", 'a') as f_out:
            f_out.write(json.dumps(postag_dict_new,ensure_ascii=False))
            f_out.write("\n")
# print(all_entity)
