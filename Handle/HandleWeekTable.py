# coding=utf-8

import re

# path = r'D:\RepoForCommunication\tyx\Python\Timetable\\'
path = '..\\'
dayTableList = [[],[],[],[],[],[],[]]
def Handle(wk_table):
    cnt = 0
    tmp = ""
    dy = 0
    TableList = wk_table.split(';')
    xq = [re.compile(r"星期一"), re.compile(r"星期二"), re.compile(r"星期三"), re.compile(r"星期四"), re.compile(r"星期五"), re.compile(r"星期六"), re.compile(r"星期日")]
    mt = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    for day in xq:
        for course in TableList:
            if (day.search(course) != None):
                dayTableList[dy].append(course)
        dy += 1
    dy = 0
    for tm_day in mt:
        ctr = 0
        for dday in dayTableList[dy]:
            flag = 0
            dday.strip('\n')
            substi_ = dday.split(" ")
            dday = ""
            dday += substi_[0]
            for ite in substi_:
                if flag != 0:
                    dday += " " + ite
                    flag -= 1
                if (mt[dy] == ite):
                    dday += " " + ite
                    flag = 2
            ans = dday.split(",")
            dayTableList[dy][ctr] = ans[0]
            ctr += 1
        dy += 1
    with open(path + 'Table.txt', 'w', encoding='utf-8') as wrt:
        for item1 in dayTableList:
            try:
                tmp = item1[0]
            except:
                pass
            for item in item1:
                if (cnt != 0 and item != tmp or cnt == 0):
                    wrt.writelines(item + '\n')
                cnt += 1
                tmp = item
            wrt.writelines('\n')
            cnt = 0