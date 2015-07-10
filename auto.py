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


class IECom():

    """open IE and use IE to auto lock bill"""

    url = 'http://ifeidai.com/EDaiWeb/AgentLoan/Login'
    fast_url = 'http://ifeidai.com/EDaiWeb/AgentLogon/MySaleApplyBill?Length=10'
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
        self.open()

    def open(self):
        '''
        open IE
        '''
        self.__ie = DispatchEx('InternetExplorer.Application')
        self.__ie.visible = 1
        self.__ie.navigate(self.url)
        self.wait()
        self.document = self.__ie.Document

    def login(self, usr_name, usr_pwd):
        '''
        login success return 1
        '''
        self.__ie.navigate(self.url)
        self.wait()
        self.reset_flag()
        self.document.getElementsByTagName('input')[0].value = usr_name
        self.document.getElementsByTagName('input')[1].value = usr_pwd
        while(self.identify() == ''):
            pass
        self.document.getElementsByTagName('input')[2].value = self.identify()
        self.document.getElementById('btnSave').click()
        self.wait()
        flag = self.get_flag()
        if flag == 't':
            sleep(2)
            self.__ie.navigate(self.fast_url)
            self.wait()
            self.document.getElementById('FastRecommend').click()
            self.wait()
            return 1
        else:
            print('Error: Can not log in ' + flag)
            print('usr_name = ' + usr_name)
            print('usr_pwd = ' + usr_pwd)
            return 0

    def identify(self):
        return self.document.getElementById('ValidateValue').value

    def reset_flag(self):
        flag = self.document.getElementById(
            'DataNotFound').getElementsByTagName('p')
        if flag.length > 0:
            flag[0].innerHTML = 't'

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
        while self.__ie.Busy or self.__ie.ReadyState != 4:
            sleep(1)

    def quit(self):
        self.__ie.quit()

    def auto(self):
        result = open(self.result_file)
        usr = open(self.usr_file)
        result_info = result.readlines()
        usr_info = usr.readlines()
        while usr_info:
            usr_name, usr_pwd = usr_info.pop().split(',')
            if self.login(usr_name, usr_pwd) == 0:
                continue
            while result_info:
                info_name, info_id, info_phone, info_city = result_info.pop().split(
                    ',')
                if info_city in city_name:
                    if self.input(info_name, info_id, info_phone):
                        break
                else:
                    break
            else:
                break
        result.close()
        usr.close()

    def input(self, info_name, info_id, info_phone):
        tmp_doc = self.document.getElementById(
            'BusinessShowDiv').contentWindow.document
        tmp_doc.getElementById('txtIDCardNO').value = info_id
        tmp_doc.getElementById('txtMobile').value = info_phone
        tmp_doc.getElementById('txtCustomerName').value = info_name
        tmp_doc.getElementById('btnAdd').click()
        self.wait()
        sleep(1)
        tmp = tmp_doc.getElementById(
            'DataNotFound').getElementsByTagName('p')
        tmp_button = tmp_doc.getElementsByTagName('button')
        if tmp.length > 0:
            tmp = tmp[0].innerHTML
            if u'上限' in tmp:
                return 1
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

try:
    test = IECom()
    test.auto()
except Exception, e:
    test.quit()
    print 'err:', e
    pass

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
