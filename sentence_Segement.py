import re
f_in = open("颐和园.txt",'r',encoding = 'utf-8')

origin_sentences = ''.join(f_in.read().split())
origin_sentences = re.split('[。？！; =]',origin_sentences)
with open("result\\sentence.txt", 'a',encoding='utf-8') as f_out:
    try:
        for i in origin_sentences:
            if len(i)==0:
                continue
            else:
                f_out.write(i+"\n")

        f_out.write('\n')
        f_out.flush()
    except Exception as e:
        raise
    finally:
        f_out.close()
print(origin_sentences)