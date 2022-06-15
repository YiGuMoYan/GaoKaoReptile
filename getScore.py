import json
import time

import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url1 = 'https://www.gaokao.cn/special/'
url2 = '?sort=2&special_type=3&year='
url3 = '&kelei=1'

year = ['2021', '2020', '2019', '2018', '2017']


def cookiesStrtoDir(cook: str):
    cookiesDir = {}
    for i in cook.split('; '):
        cookiesDir[i.split('=')[0]] = i.split('=')[1]
    cookiesDir['name'] = ''
    cookiesDir['value'] = ''
    return cookiesDir


def getCode():
    html = driver.execute_script('return document.documentElement.outerHTML;')
    html = html.encode('utf-8').decode('utf-8')
    return html


def analysisCode(html):
    htmlBs = BeautifulSoup(html, 'html.parser')
    if htmlBs.find(class_='noData')['style'] == 'display: block;':
        driver.refresh()
        time.sleep(5)
        html = getCode()
        analysisCode(html)
    else:
        schoolList = htmlBs.find_all(class_='name_des')
        for school in schoolList:
            schoolBs = BeautifulSoup(str(school), 'html.parser')
            schoolName = schoolBs.find(class_='float_l set_hoverl am_l').string
            schoolScore = schoolBs.find_all(class_='tag_item')
            schoolScore = schoolScore[len(schoolScore) - 1].string.split('：')[1]
            schoolDir[schoolName] = schoolScore
            print(schoolName + '：' + schoolScore)


def getWebNum(html):
    htmlBs = BeautifulSoup(html, 'html.parser')

    if htmlBs.find(class_='noData')['style'] == 'display: block;' and len(
            htmlBs.find_all(class_='ant-pagination')) == 0:
        print('未找到页面，重现加载...')
        driver.refresh()
        time.sleep(7)
        html = getCode()
        getWebNum(html)
    else:
        if 0 < len(htmlBs.find_all(class_='public_list_item public_tbl')) < 10:
            return 1
        ui = htmlBs.find(class_='ant-pagination').find_all('li')
        webNumber = int(ui[len(ui) - 2]['title'])
        return webNumber


def writeExcel():
    workbook = xlsxwriter.Workbook(subjectName + '.xlsx')
    for key, value in allSchoolDir.items():
        worksheet = workbook.add_worksheet(str(key))
        worksheet.activate()
        worksheet.write_row('A1', ('学校', '最低分/最低位次'))
        num = 2
        for i, j in value.items():
            worksheet.write_row('A' + str(num), (i, j))
            num += 1
    workbook.close()


if __name__ == '__main__':
    subjectName = str(input('请输入专业：'))
    subjectJson = json.loads(open('init.json', 'r+').read())
    isfind = False
    for subject in subjectJson['subject']:
        if subjectName == subject['name']:
            isfind = True
            print('初始化...')
            print('专业昵称：' + subject['name'])
            print('专业分类：' + subject['classify'])
            print('专业学位：' + subject['degree'])
            # 设置 Chorme
            chromeOptions = webdriver.ChromeOptions()
            # 禁用日志打印
            chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
            chromeOptions.add_argument('--headless')
            chromeOptions.add_argument('--disable-gpu')
            driver = webdriver.Chrome(executable_path=r'E:\Driver\chromedriver.exe', options=chromeOptions)
            allSchoolDir = {}
            for y in year:
                schoolDir = {}
                yearUrl = url1 + str(subject['id']) + url2 + y + url3
                driver.get(url=yearUrl)
                html = getCode()
                webNum = getWebNum(html)
                while True:
                    if str(type(webNum)) == '<class \'NoneType\'>':
                        html = getCode()
                        webNum = getWebNum(html)
                    else:
                        break
                print('开始爬取 ' + y + ' 信息...')
                for i in range(int(webNum)):
                    classStr = 'ant-pagination-item.ant-pagination-item-' + str(i + 1)
                    if not (i == 0):
                        driver.find_element(By.CLASS_NAME, classStr).click()
                    time.sleep(1)
                    html = getCode()
                    analysisCode(html)
                allSchoolDir[y] = schoolDir
            writeExcel()
            break
    if not isfind:
        print('未找到该专业，请核对后重试...')
