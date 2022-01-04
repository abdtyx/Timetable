# coding=utf-8
from API.DayTableInfoAPI import GetDayTable
import os
import time

not_debug = True


def main():
    text = GetDayTable()
    # if not_debug:
        # os.system('cls')
        # os.system('chdir')
    if text != "":
        print(text)
    else:
        print("您今天没有任何课程，请好好享受难得的假期。")
    '''
    对接Bot_Azure
    '''

    while (1):
        print("课表查询完毕，请关闭窗口或者同时按下Ctrl+C")
        time.sleep(10)
    # 安装为.exe程序之前解开此条并且更改三个Path路径，语句如下：
    # path = r'D:\Backup\Transmit\Timetable\\'






if __name__ == "__main__":
    main()