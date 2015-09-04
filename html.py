#!/usr/bin/env python
# -*- coding=cp936 -*-
# Copyright (C) 2015 Yeoman Zhuang

"""
html get name,id and phone
use module re to find phone number and Id number
file name such as "xxx-----3702...902.html"
@author: Yeoman
"""

import os
import re
import sys
import shutil
import pyExcelerator
import Tkinter
import tkFileDialog

version = 7


def delete_gap_dir(di):
    if os.path.isdir(di):
        for d in os.listdir(di):
            delete_gap_dir(di + os.sep + d)

        if not os.listdir(di):
            os.rmdir(di)
            print('移除空目录: ' + di)


class HTML():

    """docstring for HTML"""

    def __init__(self):
        self.curPath = os.getcwd()
        self.root = Tkinter.Tk()
        self.root.title(u"提取文件")
        self.entry = Tkinter.Entry(self.root, width=40)
        self.entry.pack(side=Tkinter.TOP, anchor="nw")
        button = Tkinter.Button(self.root, text=u"打开目录", command=self.callback)
        button.pack(side=Tkinter.TOP, anchor="nw")
        button_start = Tkinter.Button(
            self.root, text=u'开始提取', command=self.start)
        button_start.pack(side=Tkinter.TOP, anchor='nw')
        button_ = Tkinter.Button(self.root, text=u'退出', command=self.quit)
        button_.pack(side=Tkinter.RIGHT, anchor='nw')
        self.root.mainloop()

    def callback(self):
        self.entry.delete(0, Tkinter.END)  # 清空entry里面的内容
        # 调用filedialog模块的askdirectory()函数去打开文件夹
        filepath = tkFileDialog.askdirectory()
        self.curPath = filepath.encode('gbk')
        if filepath:
            self.entry.insert(0, filepath)  # 将选择好的路径加入到entry里面

    def quit(self):
        delete_gap_dir(self.curPath)
        self.root.destroy()

    def start(self):
        city_name = ['北京市', '上海市', '天津市', '重庆市', '石家庄市', '太原市', '呼和浩特市',
                     '唐山市', '大同市', '包头市', '秦皇岛市', '阳泉市', '乌海市', '邯郸市',
                     '长治市', '赤峰市', '邢台市', '晋城市', '呼伦贝尔市', '保定市', '朔州市',
                     '通辽市', '张家口市', '忻州市', '乌兰察布市', '承德市', '吕梁市',
                     '鄂尔多斯市', '沧州市', '晋中市', '巴彦淖尔市', '廊坊市', '临汾市',
                     '衡水市', '运城市', '哈尔滨市', '长春市',
                     '沈阳市', '齐齐哈尔市', '吉林市', '大连市', '牡丹江市', '四平市', '鞍山市',
                     '佳木斯市', '辽源市', '抚顺市', '大庆市', '通化市', '本溪市', '伊春市',
                     '白山市', '丹东市', '鸡西市', '白城市', '锦州市', '鹤岗市', '松原市',
                     '营口市', '双鸭山市', '阜新市', '七台河市', '辽阳市', '绥化市', '盘锦市',
                     '黑河市', '铁岭市', '朝阳市', '葫芦岛市', '南京市', '杭州市', '合肥市',
                     '福州市', '南昌市', '济南市', '无锡市', '宁波市', '芜湖市', '莆田市',
                     '赣州市', '青岛市', '徐州市', '温州市', '蚌埠市', '泉州市', '宜春市',
                     '淄博市', '常州市', '绍兴市', '淮南市', '厦门市', '吉安市', '枣庄市',
                     '苏州市', '湖州市', '马鞍山市', '漳州市', '上饶市', '东营市', '南通市',
                     '嘉兴市', '淮北市', '龙岩市', '抚州市', '烟台市', '连云港市', '金华市',
                     '铜陵市', '三明市', '九江市', '潍坊市', '淮安市', '衢州市', '安庆市',
                     '南平市', '景德镇市', '济宁市', '盐城市', '台州市', '黄山市', '宁德市',
                     '萍乡市', '泰安市', '扬州市', '丽水市', '阜阳市', '新余市', '威海市',
                     '镇江市', '舟山市', '宿州市', '鹰潭市', '日照市', '泰州市', '滁州市',
                     '滨州市', '宿迁市', '六安市', '德州市', '宣城市', '聊城市', '亳州市',
                     '临沂市', '池州市', '菏泽市', '莱芜市', '郑州市', '武汉市', '长沙市',
                     '开封市', '黄石市', '株洲市', '洛阳市', '十堰市', '湘潭市', '商丘市',
                     '荆州市', '衡阳市', '安阳市', '宜昌市', '邵阳市', '平顶山市', '襄阳市',
                     '岳阳市', '新乡市', '鄂州市', '张家界市', '焦作市', '荆门市', '益阳市',
                     '濮阳市', '黄冈市', '常德市', '许昌市', '孝感市', '娄底市', '漯河市',
                     '咸宁市', '郴州市', '三门峡市', '随州市', '永州市', '鹤壁市', '怀化市',
                     '周口市', '驻马店市', '南阳市', '信阳市', '济源市', '广州市', '南宁市',
                     '海口市', '深圳市', '柳州市', '三亚市', '珠海市', '桂林市', '汕头市',
                     '梧州市', '佛山市', '北海市', '韶关市', '崇左市', '湛江市', '来宾市',
                     '肇庆市', '贵港市', '江门市', '贺州市', '茂名市', '玉林市', '惠州市',
                     '百色市', '梅州市', '河池市', '汕尾市', '钦州市', '河源市', '防城港市',
                     '阳江市', '清远市', '东莞市', '中山市', '潮州市', '揭阳市', '云浮市',
                     '成都市', '贵阳市', '昆明市', '拉萨市', '绵阳市', '六盘水市', '昭通市',
                     '自贡市', '遵义市', '曲靖市', '攀枝花市', '安顺市', '玉溪市', '泸州市',
                     '普洱市', '德阳市', '保山市', '广元市', '丽江市', '遂宁市', '临沧市',
                     '内江市', '乐山市', '资阳市', '宜宾市', '南充市', '达州市', '雅安市',
                     '广安市', '巴中市', '眉山市', '西安市', '兰州市', '西宁市', '银川市',
                     '乌鲁木齐市', '宝鸡市', '嘉峪关市', '石嘴山市', '克拉玛依市', '咸阳市',
                     '金昌市', '吴忠市', '铜川市', '白银市', '固原市', '渭南市', '天水市',
                     '中卫市', '汉中市', '酒泉市', '安康市', '张掖市', '商洛市', '武威市',
                     '延安市', '定西市', '榆林市', '陇南市', '平凉市', '庆阳市',
                     '北京', '上海', '天津', '重庆', '石家庄', '太原', '呼和浩特',
                     '唐山', '大同', '包头', '秦皇岛', '阳泉', '乌海', '邯郸', '长治', '赤峰',
                     '邢台', '晋城', '呼伦贝尔', '保定', '朔州', '通辽', '张家口',
                     '忻州', '乌兰察布', '承德', '吕梁', '鄂尔多斯', '沧州', '晋中',
                     '巴彦淖尔', '廊坊', '临汾', '衡水', '运城', '哈尔滨', '长春',
                     '沈阳', '齐齐哈尔', '吉林', '大连', '牡丹江', '四平', '鞍山',
                     '佳木斯', '辽源', '抚顺', '大庆', '通化', '本溪', '伊春',
                     '白山', '丹东', '鸡西', '白城', '锦州', '鹤岗', '松原',
                     '营口', '双鸭山', '阜新', '七台河', '辽阳', '绥化', '盘锦',
                     '黑河', '铁岭', '朝阳', '葫芦岛', '南京', '杭州', '合肥',
                     '福州', '南昌', '济南', '无锡', '宁波', '芜湖', '莆田',
                     '赣州', '青岛', '徐州', '温州', '蚌埠', '泉州', '宜春',
                     '淄博', '常州', '绍兴', '淮南', '厦门', '吉安', '枣庄',
                     '苏州', '湖州', '马鞍山', '漳州', '上饶', '东营', '南通',
                     '嘉兴', '淮北', '龙岩', '抚州', '烟台', '连云港', '金华',
                     '铜陵', '三明', '九江', '潍坊', '淮安', '衢州', '安庆',
                     '南平', '景德镇', '济宁', '盐城', '台州', '黄山', '宁德',
                     '萍乡', '泰安', '扬州', '丽水', '阜阳', '新余', '威海',
                     '镇江', '舟山', '宿州', '鹰潭', '日照', '泰州', '滁州',
                     '滨州', '宿迁', '六安', '德州', '宣城', '聊城', '亳州',
                     '临沂', '池州', '菏泽', '莱芜', '郑州', '武汉', '长沙',
                     '开封', '黄石', '株洲', '洛阳', '十堰', '湘潭', '商丘',
                     '荆州', '衡阳', '安阳', '宜昌', '邵阳', '平顶山', '襄阳',
                     '岳阳', '新乡', '鄂州', '张家界', '焦作', '荆门', '益阳',
                     '濮阳', '黄冈', '常德', '许昌', '孝感', '娄底', '漯河',
                     '咸宁', '郴州', '三门峡', '随州', '永州', '鹤壁', '怀化',
                     '周口', '驻马店', '南阳', '信阳', '济源', '广州', '南宁',
                     '海口', '深圳', '柳州', '三亚', '珠海', '桂林', '汕头',
                     '梧州', '佛山', '北海', '韶关', '崇左', '湛江', '来宾',
                     '肇庆', '贵港', '江门', '贺州', '茂名', '玉林', '惠州',
                     '百色', '梅州', '河池', '汕尾', '钦州', '河源', '防城港',
                     '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮',
                     '成都', '贵阳', '昆明', '拉萨', '绵阳', '六盘水', '昭通',
                     '自贡', '遵义', '曲靖', '攀枝花', '安顺', '玉溪', '泸州',
                     '普洱', '德阳', '保山', '广元', '丽江', '遂宁', '临沧',
                     '内江', '乐山', '资阳', '宜宾', '南充', '达州', '雅安',
                     '广安', '巴中', '眉山', '西安', '兰州', '西宁', '银川',
                     '乌鲁木齐', '宝鸡', '嘉峪关', '石嘴山', '克拉玛依', '咸阳',
                     '金昌', '吴忠', '铜川', '白银', '固原', '渭南', '天水',
                     '中卫', '汉中', '酒泉', '安康', '张掖', '商洛', '武威',
                     '延安', '定西', '榆林', '陇南', '平凉', '庆阳']

        nu = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-']

        curFile = []

        dstPath = self.curPath + os.sep + '分类结果'
        for allFile in os.walk(self.curPath):
            for fileName in allFile[2]:
                if '分类结果' not in allFile[0] and '未提取' not in allFile[0] and'集合' not in allFile[0]:
                    curFile.append(allFile[0] + os.sep + fileName)
        # curFile = os.listdir(curPath)
        result = open(self.curPath + os.sep + 'result.txt', 'w')

        xlsResult = pyExcelerator.Workbook()
        xlsResultSheet = xlsResult.add_sheet(u'征信记录')

        result.write('姓名,身份证,电话,城市\n')
        xlsResultSheet.write(0, 0, u'姓名')
        xlsResultSheet.write(0, 1, u'身份证')
        xlsResultSheet.write(0, 2, u'电话')
        xlsResultSheet.write(0, 3, u'城市')
        curNum = 0
        findNum = 1
        failNum = 0
        totalNum = 0
        noInfoNum = 0
        resultNum = 0
        sumNum = len(curFile)
        try:
            os.mkdir(self.curPath + os.sep + '未提取')
        except:
            print('创建未提取文件夹失败')
        try:
            os.mkdir(self.curPath + os.sep + '集合')
        except:
            print('创建集合文件夹失败')
        try:
            os.mkdir(self.curPath + os.sep + '分类结果')
        except:
            print('创建分类结果文件夹失败')
        for files in curFile:
            curNum += 1
            print(str(curNum) + '/' + str(sumNum) + '\r'),
            flag = 0
            contains = (files.find('.htm') >= 0)  # and(files.find('-') >= 0)
            if contains:
                i = 0
                tempFile = os.path.split(files)[1]
                while (tempFile[i] not in nu) and (tempFile[i] != '.'):
                    i += 1
                Id = re.search(r'\d{17}[\dX]', tempFile)
                File = open(files)
                lines = File.readlines()
                phone = ''
                if len(lines) > 394:
                    if flag == 0:
                        m = re.search(r'>0?1(3|4|5|6|7|8)\d{9}<', lines[245])
                        if m:
                            flag = 1
                            phone = m.group(0)[-12:-1]
                    if flag == 1:
                        for line in lines[270], lines[273], lines[378], lines[393]:
                            for c in city_name:
                                if c in line and flag == 1:
                                    city = c
                                    flag = 2
                                    break
                            if flag == 2:
                                break
                    if flag != 2:
                        for line in lines:
                            if m:
                                flag = 1
                                phone = m.group(0)[-12:-1]
                            else:
                                m = re.search(r'>0?1(3|4|5|6|7|8)\d{9}<', line)
                            if flag == 1:
                                for c in city_name:
                                    if c in line:
                                        flag = 2
                                        city = c
                                        break
                                if flag == 2:
                                    break
                            if flag == 2:
                                break
                    if flag == 2:
                        result.write(tempFile[:i] + ",")
                        if Id:
                            result.write(Id.group(0) + ",")
                            xlsResultSheet.write(findNum, 1, Id.group(0))
                        else:
                            result.write(",")
                        result.write(phone + ",")
                        result.write(city + "\n")
                        xlsResultSheet.write(
                            findNum, 0, tempFile[:i].decode('gbk'))
                        xlsResultSheet.write(findNum, 2, phone)
                        xlsResultSheet.write(
                            findNum, 3, city.decode('gbk'))
                        findNum += 1
                        try:
                            os.mkdir(dstPath + os.sep + city)
                        except:
                            pass
                        try:
                            shutil.copy(files, dstPath + os.sep + city)
                        except:
                            # os.remove(files)
                            failNum += 1
                            resultNum += 1
                File.close()
                if flag == 0:
                    try:
                        shutil.copy(files, self.curPath + os.sep + '未提取')
                    except:
                        # os.remove(files)
                        failNum += 1
                        noInfoNum += 1
                try:
                    shutil.move(files, self.curPath + os.sep + '集合')
                except:
                    os.remove(files)
                    failNum += 1
                    totalNum += 1

        result.close()
        xlsResult.save(self.curPath + os.sep + 'result.xls')

        print('搜索完毕！')
        print('共' + str(sumNum) + '个html文件，成功提取' + str(curNum) + '个文件')
        print('共有' + str(failNum) + '个文件重复，移动失败')
        print('其中' + str(resultNum) + '个文件在分类结果中重复'),
        print(str(noInfoNum) + '个文件在未提取中重复'),
        print(str(totalNum) + '个文件在集合中重复')

test = HTML()
