# coding=utf-8

# 接受课程列表（以'\n'区分不同日），返回周课表列表
def Split(weektable):
    dt = ["", "", "", "", "", "", ""]
    cnt = 0
    for item in weektable:
        if item == "\n":
            cnt += 1
        else:
            dt[cnt] += item
    return dt