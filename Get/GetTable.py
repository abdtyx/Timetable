# coding=utf-8

# 带Session()去访问课表url，拿到html源码，交给handle模块处理，最后存储为Table.txt，不返回任何值

import time
import json
import requests
from Login.Login import LoginEhall
from Handle.HandleWeekTable import Handle

# path = r'D:\RepoForCommunication\tyx\Python\Timetable\\'
path = '..\\'

'''
# 计算时间
# 暂时不知道如何获取当前周
# start是学期开始日，必须手动改
# 已解决
start = int(256)
f = open(path + 'time.txt', 'r')
dt = f.readlines()
tm_wk =  str(int(1) + int((int(dt[1]) - start + int(1)) / int(7))) # 周
xnxqdm = "2021-2022-1" # 学年学期
f.close()
'''

def Table(userinfo, s):
    LoginTimes = 0
    '''
    with open(path + 'Table.txt', 'w') as table:
        for i in range(0, 7):
            table.writelines("Testing...\n")
    '''
    r = s.post("http://ehall.xjtu.edu.cn/jwapp/sys/wdkb/modules/jshkcb/dqxnxq.do")
    data = json.loads(r.text)
    xnxqdm = data['datas']['dqxnxq']['rows'][0]['DM']
    xn = data['datas']['dqxnxq']['rows'][0]['XNDM']
    xq = data['datas']['dqxnxq']['rows'][0]['XQDM']
    localtime = time.localtime(time.time())
    rq = str(localtime.tm_year) + '-' + str(localtime.tm_mon) + '-' + str(localtime.tm_mday)
    d = {
        "XN": xn,
        "XQ": xq,
        "RQ": rq,
    }
    r = s.post("http://ehall.xjtu.edu.cn/jwapp/sys/wdkb/modules/jshkcb/dqzc.do", data=d)
    data = json.loads(r.text)
    tm_wk = data['datas']['dqzc']['rows'][0]['ZC']
    r = s.post("http://ehall.xjtu.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do?XNXQDM=" + str(xnxqdm) + "&SKZC=" + str(tm_wk), allow_redirects=False)
    while (r.status_code != 200):
        s = LoginEhall(userinfo, s)
        '''
        r = s.post("http://ehall.xjtu.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do", data=xskcb_payload, allow_redirects=False)
        '''
        r = s.post("http://ehall.xjtu.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do?XNXQDM=2021-2022-1&SKZC=5", allow_redirects=False)
        LoginTimes += 1
        if (LoginTimes == 5):
            # SendMail("登录失败")
            print("登录失败")
    data = json.loads(r.text)
    # print(r.text)
    rstr = ""
    for item in data['datas']['xskcb']['rows']:
        rstr += str(item['KCM']) + " " + str(item['YPSJDD']) + ";"
    # SendMail(rstr)
    print("课表查询完毕")
    Handle(rstr)    
