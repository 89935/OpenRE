
def open_file(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
    except:
        print("您输入的文件路径错误！")
        return 0
    else:
        return f


def close_file(filename):
    filename.close()

# """
# D:\PyCharmProjects\entity_verb\entity_verb_result\context_word_freq_dict_v2.json
# 请输入第二个文件的绝对路径：C:\Users\thinkpad\Desktop\结果文件\02-13结果文件\context_word_freq_dict_v2.json
# """

def compare(filename1, filename2):
    line = 0
    index = 0
    while True:
        str1 = filename1.readline()
        str2 = filename2.readline()
        line += 1
        if str1 != "" or str2 != "":
            if str1 != str2:
                if len(str1) > len(str2):
                    for i in range(len(str2)):
                        index += 1
                        if str1[i] != str2[i]:
                            print("两个文件第一次出现不同在：{}行{}列".format(line, index))
                            print(str1[i-20:i+4]+"   "+str2[i-20:i+4])
                            return 0
                        else:
                            continue
                else:
                    for i in range(len(str1)):
                        index += 1
                        if str1[i] != str2[i]:
                            print("两个文件第一次出现不同在：{}行{}列".format(line, index))
                            print(str1[i - 100:i + 100] + "   " + str2[i - 100:i + 100])
                            return 0
                        else:
                            continue
        elif str1 == "" and str2 == "":
            print("两个文件相同")
            break


if __name__ == '__main__':
    filename1 = input("请输入第一个文件的绝对路径：")
    f1 = open_file(filename1)
    if f1 == 0:
        exit(0)
    else:
        filename2 = input("请输入第二个文件的绝对路径：")
        f2 = open_file(filename2)
    if f2 == 0:
        f1.close_file()
        exit(0)
    compare(f1, f2)

    # D:\PyCharmProjects\entity_verb\entity_verb_result\context_only_word_freq_dict03-16修改了循环方法.json
    # D:\PyCharmProjects\entity_verb\entity_verb_result\context_word_freq_dict_v4_beforeAndAfter.json
    # D:\PyCharmProjects\entity_verb\entity_verb_result
    # D:\PyCharmProjects\entity_verb\entity_verb_result\intersection_only_verb03-16修改了循环方法.csv
    # D:\PyCharmProjects\entity_verb\entity_verb_result\intersection_only_verb_windowWord_1_beforeAndAfter.csv