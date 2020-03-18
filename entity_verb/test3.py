import json
# f = open("D:\python-file\北京市旅游知识图谱\\"
#          , 'r', encoding='utf-8')
# # file = f.read()
# # json_file = json.loads(file)
# for line in f.readlines():
#     json_line = json.loads(line)
#     print(json_line)


def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    # ax = sum()
    return sum

print(lazy_sum(1, 3, 5, 7, 9)())
# print(f)

def calc_sum(*args):
    ax = 0
    for n in args:
        ax = ax + n
    return ax

calc_sum(1)
