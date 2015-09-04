#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Copyright (C) 2015 Yeoman Zhuang

"""
自动锁单
"""
# import time
from win32com.client import DispatchEx
# from win32com.client import Dispatch
from time import sleep
from uuid import getnode
import os
import Tkinter as tk
import tkFileDialog

import sys
# 获取脚本文件的当前路径


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


class IECom():

    """open IE and use IE to auto lock bill"""

    url = 'http://ifeidai.com/EDaiWeb/AgentLoan/Login'
    fast_ur = 'http://ifeidai.com/EDaiWeb/AgentLogon/MySaleApplyBill?Length=10'
    result_file = 'result.txt'
    usr_file = 'login.txt'
    city_name = [u'青岛', u'济南', u'唐山', u'无锡', u'上海', u'扬州',
                 u'深圳', u'武汉', u'石家庄', u'北京', u'南昌', u'海口',
                 u'惠州', u'成都', u'南京', u'广州', u'中山', u'郑州',
                 u'南宁', u'佛山', u'长沙', u'重庆', u'西安', u'贵阳',
                 u'厦门', u'青岛市', u'济南市', u'唐山市', u'无锡市',
                 u'上海市', u'扬州市', u'深圳市', u'武汉市', u'石家庄市',
                 u'北京市', u'南昌市', u'海口市', u'惠州市', u'成都市',
                 u'南京市', u'广州市', u'中山市', u'郑州市', u'南宁市',
                 u'佛山市', u'长沙市', u'重庆市', u'西安市', u'贵阳市',
                 u'厦门市']

    def __init__(self):
        '''
        init open IE
        '''
        code = getnode()
        self.code_license = code % 3721 + code * 9997 % 997
        self.root = cur_file_dir()
        try:
            lic = open(self.root + os.sep + 'lic')
            line = lic.readline()
            lic.close()
        except:
            line = u'请输入激活码'
        self.main_window = tk.Tk()
        self.main_window.minsize(300, 300)
        self.main_window.title(u'锁单神器')
        self.main_window.protocol('WM_DELETE_WINDOW', self.quit)
        win = tk.Frame()
        self.entry_var = tk.StringVar()
        self.entry_var.set(line)
        self.result_var = tk.StringVar()
        self.result_var.set(u'信息文件路径：    ' + self.result_file)
        self.mac_var = tk.StringVar()
        self.mac_var.set(u'机器码:    ' + str(code))
        self.usr_var = tk.StringVar()
        self.usr_var.set(u'账户文件路径：    ' + self.usr_file)
        self.info_str = u'''
        锁单神器v7：自动将信息文件中的数据锁到账户文件中的账户中。
        信息文件格式：姓名,身份证号,手机号,城市名
        例如：张三,100000000000000000,11100000000,北京
        账户文件格式：账户名,密码
        例如：100000000000000000,a111111


        Copyright (C) 2015 Yeoman Zhuang
        '''
        self.info_var = tk.StringVar()
        self.info_var.set(self.info_str)
        win.pack()
        label_mac = tk.Entry(win, textvariable=self.mac_var)
        label_mac.pack(side=tk.TOP)
        self.entry_en = tk.Entry(win, textvariable=self.entry_var)
        self.entry_en.pack(side=tk.TOP)
        label_result = tk.Label(win, textvariable=self.result_var)
        label_result.pack(side=tk.TOP)
        label_usr = tk.Label(win, textvariable=self.usr_var)
        label_usr.pack(side=tk.TOP)
        label_info = tk.Label(win, textvariable=self.info_var)
        label_info.pack(side=tk.BOTTOM)
        button_act = tk.Button(win, text=u'激活', command=self.act)
        button_act.pack(side=tk.LEFT)
        self.button_set_result = tk.Button(
            win, text=u'打开信息文件', command=self.set_result, state=tk.DISABLED)
        self.button_set_result.pack(side=tk.LEFT)
        self.button_set_usr = tk.Button(
            win, text=u'打开账户文件', command=self.set_info, state=tk.DISABLED)
        self.button_set_usr.pack(side=tk.LEFT)
        # self.button_open = tk.Button(
        # win, text=u'打开IE', command=self.open, state=tk.DISABLED)
        # self.button_open.pack(side=tk.LEFT)
        self.button_start = tk.Button(
            win, text=u'开始锁单', command=self.open_auto, state=tk.DISABLED)
        self.button_start.pack(side=tk.LEFT)

        win.mainloop()

    def open_auto(self):
        self.open()
        self.auto()

    def act(self):
        if str(self.code_license) == self.entry_en.get():
            self.button_start['state'] = tk.NORMAL
            self.button_set_usr['state'] = tk.NORMAL
            self.button_set_result['state'] = tk.NORMAL
            # self.button_open['state'] = tk.NORMAL
            lic = open(self.root + os.sep + 'lic', 'w')
            lic.write(str(self.code_license))
            lic.close()
            self.entry_var.set(u'激活成功')
        else:
            self.entry_var.set(u'激活失败，请重新输入')

    def set_result(self):
        self.result_file = tkFileDialog.askopenfilename(initialdir='D:/')
        self.result_var.set(u'信息文件路径：    ' + self.result_file)

    def set_info(self):
        self.usr_file = tkFileDialog.askopenfilename(initialdir='D:/')
        self.usr_var.set(u'账户文件路径：    ' + self.usr_file)

    def open(self):
        '''
        open IE
        '''
        print(u'打开登陆账号文件和信息文件')
        self.result = open(self.result_file)
        self.usr = open(self.usr_file)
        print(u'绑定IE')
        self.__ie = DispatchEx('InternetExplorer.Application')
        self.__ie.visible = 1
        self.__ie.navigate(self.url)
        self.wait()
        self.document = self.__ie.Document

    def login(self, usr_name, usr_pwd):
        '''
        login success return 1
        '''
        print('Login:' + usr_name)
        self.__ie.navigate(self.url)
        self.wait()
        # self.reset_flag()
        print(u'输入账户密码')
        self.document.Body.getElementsByTagName('input')[0].value = usr_name
        self.document.getElementsByTagName('input')[1].value = usr_pwd
        while(self.identify() == ''):
            pass
        self.document.getElementsByTagName('input')[2].value = self.identify()
        self.document.getElementById('btnSave').click()
        self.wait()
        flag = 't'
        if flag == 't':
            print(u'登陆成功！')
            sleep(2)
            self.__ie.navigate(self.fast_ur)
            self.wait()
            self.document.getElementById('FastRecommend').click()
            print(u'开始快速推荐')
            self.wait()
            return 1
        else:
            print('Error: Can not log in ' + flag)
            print('usr_name = ' + usr_name)
            print('usr_pwd = ' + usr_pwd)
            return 0

    def identify(self):
        print(u'获得验证码')
        return self.document.getElementById('ValidateValue').value

    # def reset_flag(self):
    #     flag = self.document.getElementById(
    #         'DataNotFound').getElementsByTagName('p')
    #     if flag.length > 0:
    #         flag[0].innerHTML = 't'

    def get_flag(self):
        flag = self.document.getElementById(
            'DataNotFound')
        if flag:
            flag = flag.getElementsByTagName('p')
            if flag.length > 0:
                return flag[0].innerHTML
        return 't'

    def visible(self):
        self.__ie.Visible = 1 - self.__ie.Visible

    def wait(self):
        print(u'等待中')
        while self.__ie.Busy or self.__ie.ReadyState != 4:
            sleep(1)

    def nwait(self):
        while not self.__ie.Busy or self.__ie.ReadyState == 4:
            sleep(1)

    def quit(self):
        print(u'退出')
        self.main_window.destroy()
        self.__ie.quit()

    def auto(self):
        result_info = self.result.readlines()
        usr_info = self.usr.readlines()
        while usr_info:
            usr_name, usr_pwd = usr_info.pop().split(',')
            if self.login(usr_name, usr_pwd) == 0:
                continue
            while result_info:
                line = result_info.pop()
                print(u'录入' + line[:-1].decode('gbk'))
                info_name, info_id, info_phone, info_city = line.split(',')
                info_name = info_name.decode('gbk')
                info_city = info_city[:-1].decode('gbk')
                if info_city in self.city_name:
                    # if True:
                    if self.input(info_name, info_id, info_phone):
                        result_info.append(line)
                        break
            else:
                break
        print(u'录入完成')
        self.result.close()
        self.usr.close()
        if(len(result_info) > 0):
            print(u'账号已用完，未录入信息在result.txt中')
            result = open(self.result_file, 'w')
            for line in result_info:
                result.write(line)
            result.close()

    def input(self, info_name, info_id, info_phone):
        print(u'输入信息')
        tmp_doc = self.document.getElementById(
            'BusinessShowDiv').contentWindow.document
        tmp_doc.getElementById('txtIDCardNO').value = info_id
        tmp_doc.getElementById('txtMobile').value = info_phone
        tmp_doc.getElementById('txtCustomerName').value = info_name
        tmp_doc.getElementById('btnAdd').click()
        sleep(2)
        self.wait()
        tmp = tmp_doc.getElementById(
            'DataNotFound').getElementsByTagName('p')
        while tmp.length == 0:
            tmp = tmp_doc.getElementById(
                'DataNotFound').getElementsByTagName('p')
        if tmp.length > 0:
            tmp = tmp[0].innerHTML
            if u'该客户可提交贷款' in tmp:
                print(u'可提交贷款')
                tmp_button = tmp_doc.getElementsByTagName('button')
                tmp_button[0].click()
                sleep(1)
                tmp_button = tmp_doc.getElementsByTagName('button')
                tmp_button[0].click()
                sleep(2)
                self.wait()
                tmp_doc.getElementById('btnContinuance').click()
                self.wait()
                return 0
            if u'上限' in tmp:
                print(u'推荐数量达到上限')
                return 1
        tmp_button = tmp_doc.getElementsByTagName('button')
        # while tmp_button.length == 0:
        # tmp_button = tmp_doc.getElementsByTagName('button')
        tmp_button[0].click()
        return 0

    def get_nodes(self, parent_node, tag):
        """
        >>> coldiv=GetNodes(body,"div")
        """
        child_nodes = []
        for childNode in parent_node.getElementsByTagName(tag):
            child_nodes.append(childNode)
        return child_nodes

    def node_by_attr(self, nodes, nodeattr, nodeval):
        """
        >>> div_id_editor=node_by_attr(coldiv,"id","editor_ifr")
        """
        for node in nodes:
            if str(node.getAttribute(nodeattr)) == nodeval:
                return node
        return None

    def set_node(self, node, val):
        node.innerHTML = val

test = IECom()


# def start_office_application(app_name):
# 在这里获取到app后，其它的操作和通过VBA操作办公软件类似
#     app = Dispatch(app_name)
#     app.Visible = True
#     time.sleep(0.5)
#     app.Quit()
# if __name__ == '__main__':
#     '''
#     通过python启动办公软件的应用进程，
#     其中wps、et、wpp对应的是金山文件、表格和演示
#     word、excel、powerpoint对应的是微软的文字、表格和演示
#     '''
#     lst_app_name = [
#         "wps.Application",
#         'et.Application',
#         'wpp.Application',
#         'word.Application',
#         'excel.Application',
#         'powerpoint.Application'
#     ]
#     for app_name in lst_app_name:
#         print "app_name:%s" % app_name
#     start_office_application(app_name)

# while 1:
#     state = ie.ReadyState==4break
#     print state
#     sleep(1)

# 验证码是显式的，也是醉了，所以不需要OCR了
# self.document.getElementById('changeValidateImage').click()
# sleep(5)
# img_src = self.document.images[10].src
# print 'download images'
# img_data = urlopen(img_src)
# img_byte = img_data.read()
# img_file = open('temp.gif', 'wb')
# img_file.write(img_byte)
# img_file.close()
# img = Image.open('temp.gif')
# img = img.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(img)
# img = enhancer.enhance(2)
# img = img.convert('1')
# img.crop((2, 2, 72, 30)).save("temp.bmp", dpi=(200, 200))
# remove('temp.gif')
# args = ['tesseract', 'temp.bmp', 'temp']
# print 'OCRing'
# proc = Popen(args)
# proc.wait()
# inf = file('temp.txt')
# text = inf.read()
# inf.close()
# remove('temp.txt')
# remove('temp.bmp')
# text_list = text.split(' ')
# for txt in text_list:
#     if len(txt) >= 4:
#         return txt[:4]
