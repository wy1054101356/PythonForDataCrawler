import xlrd
import urllib.request
import urllib
import re
import xlwt
import numpy
from xlrd import open_workbook
from xlutils.copy import copy


url = "https://you.ctrip.com/sight/shiyan464/s0-p2.html#sightname"
webSourceCode = urllib.request.urlopen(url).read().decode("utf-8","ignore")


# 匹配数据的正则表达式
sightImageRe = re.compile(r'<img src="(.*?)" width="220" height="140" img-id=".*?" />')
sightNameRe = re.compile(r'<a target="_blank" href=".*?" title=".*?">(.*?)</a>')
sightSiteRe = re.compile(r'<dd class="ellipsis">(.*?)</dd>',re.S) #s 多行任意匹配
sightRemarkRe1 = re.compile(r'<span class="sightc"><a rel="nofollow" target="_blank" href=".*?">(.*?)</a>.*?</span>.*?</p>',re.S)
sightRemarkRe2 = re.compile(r'<span class="sightc"><a rel="nofollow" target="_blank" href=".*?">.*?</a>.*?</span>(.*?)</p>',re.S)


# 匹配网页对应的标题数据
sightImages = sightImageRe.findall(webSourceCode)
sightNames = sightNameRe.findall(webSourceCode)
sightSites = sightSiteRe.findall(webSourceCode)
sightRemarks1 = sightRemarkRe1.findall(webSourceCode)
sightRemarks2 = sightRemarkRe2.findall(webSourceCode)

infoCount = len(sightImages)

print("图片" "==============================================================")
for sighetImage in sightImages:
    print("图片:" + sighetImage)

print("景点==============================================================")
for sightName in sightNames:
    print("景点:" + sightName)

print("地点==============================================================")
for sightSite in sightSites:
    print("地点:" + sightSite)

print("用户==============================================================")
for sightRemark1 in sightRemarks1:
    print("用户:" +sightRemark1)

print("评价==============================================================")
for sightRemark2 in sightRemarks2:
    print("用户:" +sightRemark2)


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")



def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


    
book_name_xls = '十堰景点.xls'
sheet_name_xls = '十堰景点'
value_title = [["图片", "景点", "地点", "用户", "评价"],]

value1 = [ [""] * len(value_title[0])  for i in range(infoCount)]

print(value1)


for i in range(len(value1)):
    value1[i][0] = sightImages[i]

for i in range(len(value1)):
    value1[i][1] = sightNames[i]

for i in range(len(value1)):
    value1[i][2] = sightSites[i]

for i in range(len(value1)):
    value1[i][3] = sightRemarks1[i]

for i in range(len(value1)):
    value1[i][4] = sightRemarks2[i]

#print(value1)
#write_excel_xls(book_name_xls, sheet_name_xls, value_title)
write_excel_xls_append(book_name_xls, value1)
