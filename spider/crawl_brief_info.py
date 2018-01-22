"""
爬取拉勾网上数据上的简要信息，并将结果存入至excel中
"""
import os
import time
import requests
import numpy
from openpyxl import Workbook

headers = {'Host': 'www.lagou.com',
           'Origin': 'https://www.lagou.com',
           'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98?px=default&city=%E5%85%A8%E5%9B%BD',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

cookies = {'JSESSIONID': '99021FFD6F8EC6B6CD209754427DEA93',
           '_gat': '1',
           'user_trace_token': '20170203041008-9835aec2-e983-11e6-8a36-525400f775ce',
           'PRE_UTM': '',
           'PRE_HOST': '',
           'PRE_SITE': '',
           'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F',
           'LGUID': '20170203041008-9835b1c9-e983-11e6-8a36-525400f775ce',
           'SEARCH_ID': 'bfed7faa3a0244cc8dc1bb361f0e8e35',
           'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1486066203',
           'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1486066567',
           '_ga': 'GA1.2.2003702965.1486066203',
           'LGSID': '20170203041008-9835b03a-e983-11e6-8a36-525400f775ce',
           'LGRID': '20170203041612-714b1ea3-e984-11e6-8a36-525400f775ce'}


def lagou_spider(url):
    """
    提交表单至url，获取返回的json格式的数据
    对数据进行清洗并返回
    """
    keyword = '数据挖掘'
    city = '全国'
    para = {'first': 'false', 'pn': '1', 'kd': keyword, 'city': city}
    position_list = []
    for i in range(1, 31):
        para['pn'] = str(i)
        response = requests.post(url, data=para, headers=headers, cookies=cookies)
        result = response.json()
        data = result['content']['positionResult']
        page_no = result['content']['pageNo']
        infos = data['result']
        for info in infos:
            position = []
            companyLabelList = info['companyLabelList']     # 职位诱惑(list)
            if len(companyLabelList) > 1:
                companyLabelList = '-'.join(companyLabelList)
            elif len(companyLabelList) == 1:
                companyLabelList = str(companyLabelList[0])
            else:
                companyLabelList = '-'
            positionLables = info['positionLables']         # 岗位技术标签(list)
            if len(positionLables) > 1:
                positionLables = '-'.join(positionLables)
            elif len(positionLables) == 1:
                positionLables = str(positionLables[0])
            else:
                positionLables = '-'
            positionId = info['positionId']                 # 职位ID
            positionName = info['positionName']             # 职位名称
            companyId = info['companyId']                   # 公司ID
            companyFullName = info['companyFullName']       # 公司全称
            companyShortName = info['companyShortName']     # 公司简称
            industryField = info['industryField']           # 公司所属行业
            city = info['city']                             # 公司地点
            companySize = info['companySize']               # 公司规模
            education = info['education']                   # 学历要求
            financeStage = info['financeStage']             # 公司融资规模
            salary = info['salary']                         # 薪水
            firstType = info['firstType']                   # 第一岗位类型
            secondType = info['secondType']                 # 第二岗位类型
            workYear = info['workYear']                     # 工作经验要求
            latitude = info['latitude']                     # 纬度
            longitude = info['longitude']                   # 经度

            position.append(positionId)
            position.append(positionName)
            position.append(education)
            position.append(salary)
            position.append(workYear)

            position.append(firstType)
            position.append(secondType)
            position.append(positionLables)
            position.append(companyLabelList)

            position.append(companyId)
            position.append(companyShortName)
            position.append(companyFullName)
            position.append(industryField)
            position.append(companySize)
            position.append(financeStage)

            position.append(city)
            position.append(latitude)
            position.append(longitude)
            position_list.append(position)

        print("爬取第%s页成功,  %s" % (i, page_no))
        time.sleep(numpy.random.rand()*15)
    return position_list


def save_excel(position_list):
    wb = Workbook()
    ws = wb.active
    ws.append(['岗位ID', '岗位名称', '学历要求', '薪水', '经验要求',
               '第一标签', '第二标签', '技术标签', '职业诱惑',
               '公司ID', '公司简称', '公司全称', '公司所属行业', '公司规模',
               '融资情况', '公司所在城市', '经度', '纬度'])
    for position in position_list:
        print(position)
        print(type(position))
        ws.append(position)
    d = os.path.dirname(__file__)
    parent_path = os.path.dirname(d)
    xlsx = os.path.join(parent_path, 'result/拉勾网_数据挖掘.xlsx')
    wb.save(xlsx)
    print("存储成功")


if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    position_list = lagou_spider(url)
    save_excel(position_list)
