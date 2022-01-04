# coding=utf-8

# from os import read
import time
import requests
import json
from Login.Login import LoginEhall
from Get.GetTable import Table
from Get.GetChangeInfo import Change
from Handle.SplitDayTable import Split
from EhallCrypto.Crypto import crypates

# path = r'D:\RepoForCommunication\tyx\Python\Timetable\\'
path = '..\\'

# 该API不需要任何参数，返回日课表（列表类型）

def GetDayTable():
    # 账号信息，密码需用加密过的
    userinfo = {}
    # flip变量标记是否已经LoginEhall
    flip = 0
    # new_user_flag变量标记今天是否有新用户登录
    new_user_flag = 0
    # netid = ""
    # password = ""
    # 选择新用户还是老用户登录，只能保存一个账号
    flag = input("是否使用原账号？(y or n)")
    if (flag == "Y" or flag == "y"):
        try:
            with open(path + 'userinfo.txt', 'r') as readuserinfo:
                userinfo["netid"] = int(readuserinfo.readline())
                userinfo["password"] = str(readuserinfo.readline()).strip('\n')
                # userinfo["memberId"] = str(readuserinfo.readline()).strip('\n')
        except Exception as err:
            print("第一次登录，请使用新账号")
            new_user_flag = 1
            userinfo["netid"] = int(input("请输入新的账号："))
            userinfo["password"] = input("请输入密码：")
            # userinfo["memberId"] = input("请输入新的memberId：")
            with open(path + 'userinfo.txt', 'w') as changeuserinfo:
                changeuserinfo.writelines(str(userinfo["netid"]) + '\n')
                changeuserinfo.writelines(userinfo["password"] + '\n')
                # changeuserinfo.writelines(userinfo["memberId"] + '\n')
    else:
        new_user_flag = 1
        userinfo["netid"] = input("请输入新的账号：")
        userinfo["password"] = input("请输入密码：")
        # userinfo["memberId"] = input("请输入新的memberId：")
        with open(path + 'userinfo.txt', 'w') as changeuserinfo:
            changeuserinfo.writelines(userinfo["netid"] + '\n')
            changeuserinfo.writelines(userinfo["password"] + '\n')
            # changeuserinfo.writelines(userinfo["memberId"] + '\n')
    # userinfo = {
    #     "netid" : netid,
    #     "password" : password
    # }

    # 前端加密API
    userinfo['password'] = crypates(userinfo['password'])

    # Login模块处理登录ehall
    s = requests.Session()
    # 获得LoginEhall返回的保持在线的cookies，用该cookies访问课表html
    # s = LoginEhall(userinfo, s)
    # LoginEhall()放外面会导致程序运行时间的期望变长
    # 检测时间，存储到文件，每周一更新一次文件中的日期，可识别是否到新的一周
    localtime = time.localtime(time.time())
    # 周课表全局变量，类型：列表
    # 周课表应为二级列表，0-6表示wday，每一个元素是当日课表的列表
    weektable = []
    # 若周一，则localtime.tm_wday == 0
    # 因为要处理time.txt，若此前不存在time.txt，将会报错，因此先初始化一个time.txt并且写入三行“-1”
    try:
        trytime = open(path + 'time.txt', 'r')
        tmp = trytime.readlines()[0]
    except Exception as result:
        print("第一次运行，正在初始化time.txt")
        trytime = open(path + 'time.txt', 'w')
        trytime.writelines("-1\n")
        trytime.writelines("-1\n")
        trytime.writelines("-1\n")
        trytime.writelines("-1\n")
        print("初始化time.txt完成")
    finally:
        trytime.close()
    # if (localtime.tm_wday == 0):
        # 若为周一，需要判断该周是否已获取了课表，若已获取，不fetch新课表
    with open(path + 'time.txt', 'r') as timer1:
        tm1 = timer1.readlines()
        tm1[0] = tm1[0].strip('\n')
        tm1[1] = tm1[1].strip('\n')
        tm1[2] = tm1[2].strip('\n')
        if (tm1[0] == str(localtime.tm_year) and localtime.tm_yday - int(tm1[1]) < 7 and localtime.tm_wday >= int(tm1[2]) and new_user_flag == 0):
            # 时间仍然在同一周，且不是新用户登录，不改时间，不获取新列表，直接拿取Table.txt的数据
            pass
        else:
            # 新一周或者新用户登录，因此更改时间，表示新的当前周
            with open(path + 'time.txt', 'w') as changetime:
                changetime.writelines(str(localtime.tm_year) + '\n')
                changetime.writelines(str(localtime.tm_yday) + '\n')
                changetime.writelines(str(localtime.tm_wday) + '\n')
                changetime.writelines("-1\n")
            # 调用GetTable抓取新课表，之后可在Table.txt获取课表信息
            # print("已重新抓取课表")
            s = LoginEhall(userinfo, s)
            flip = 1
            Table(userinfo, s)
        with open(path + 'Table.txt', 'r', encoding='utf-8') as tb2:
            weektable = tb2.readlines()
            weektable = Split(weektable)
    '''
    # 若不为周一，需看本周是否已获取新课表，若没有，则获取新课表
    else:
        with open(path + 'time.txt', 'r') as timer3:
            tm3 = timer3.readlines()
            if (tm3[0] == str(localtime.tm_year) and tm3[1] == str(localtime.tm_yday)):
                pass
            else:
                with open(path + 'time.txt', 'w') as changetime:
                    changetime.writelines(localtime.tm_year + '\n')
                    changetime.writelines(localtime.tm_yday + '\n')
                    changetime.writelines("-1\n")
                Table(cookies)
            with open(path + 'Table.txt', 'r') as tb3:
                weektable = tb3.readlines()
    '''
    # 课表获取完毕，接下来获取调课信息
    with open(path + 'time.txt', 'r') as timer2:
        tm2 = timer2.readlines()
        if (tm2[-1] != str(localtime.tm_wday)):
            # 今天没有获取调课信息
            # 覆写日期
            # print("debug")
            tm2[-1] = str(localtime.tm_wday)
            with open(path + 'time.txt', 'w') as wr:
                for date in tm2 :
                    wr.writelines(date)
            # 调用Change()调整课表
            if (flip != 1):
                s = LoginEhall(userinfo, s)
            Change(s)
            # 将weektable重赋值为新的课表信息
            with open(path + 'Table.txt', 'r', encoding='utf-8') as ChangedTable:
                weektable = ChangedTable.readlines()
                weektable = Split(weektable)
    # 注意此处从文件读入并返回无法直接给list，建议使用split分割得到的数据，也就是说依然需要一个Handle函数来split一下这个数据然后再返回给main一个字符串
    try:
        return weektable[localtime.tm_wday]
    except:
        return "您今天没有任何课程，请好好享受难得的假期。"