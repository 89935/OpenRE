import thulac
import jieba
from entity_verb.entity_verb_new import entity_verb_new

import os
from pyltp import Segmentor,SentenceSplitter,Postagger,NamedEntityRecognizer,Parser
default_model_dir = 'D:\python-file\knowledge_extraction-master-tyz\\ltp_data_v3.4.0\\' #LTP模型文件目录
segmentor = Segmentor()
user_dict = "source\\user.txt"
# segmentor_flag = segmentor.load_with_lexicon(os.path.join(default_model_dir,'cws.model'),user_dict)
segmentor_flag = segmentor.load(os.path.join(default_model_dir,'cws.model'))
postagger = Postagger()
postag_flag = postagger.load(os.path.join(default_model_dir,'pos.model'))
sentence_list = ["2005年1月北京市决定将地处朝阳区东四环原准备到土地市场上进行交易的学校,改造为附中,2006年完成搬迁"]
for sentence in sentence_list:
    words = segmentor.segment(sentence)
    pos = postagger.postag(words)
    print('\t'.join(words))
    print('\t'.join(pos))

# thu1 = thulac.thulac()
# entity_verb_new = entity_verb_new()
# print(entity_verb_new.splitWord(["缎店、点心铺、茶楼、金银首饰楼等。店铺中的店员都"],thu1))
# jieba.add_word("金银首饰",10000)
# words = jieba.cut("缎店、点心铺、茶楼、金银首饰楼等。店铺中的店员都")
# for word in words:
#     print(word)
# import jieba.posseg as pseg
# words =pseg.cut("缎店、点心铺、茶楼、金银首饰楼等。店铺中的店员都")
# for w in words:
#    print(w.word,w.flag)