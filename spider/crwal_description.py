"""
根据positionId进一步爬取更详细的信息
"""
import time
import pymysql
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'm.lagou.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Mobile Safari/537.36'
}
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


def get_position_id(cursor):
    """
    从数据库中获取position_id
    param
        cursor:数据库的游标
    return
        position_id(list): 从数据库中获取的p_id
    """
    query_sql = '''
    select positionId from lagou_crawl.posiition_info
    '''
    cursor.execute(query_sql)
    position_id = list()
    for p_id in cursor.fetchall():
        position_id.append(p_id[0])
    return position_id


def get_descriptions(position_id):
    """
    通过从数据库获取的position_id来进一步获取该职位的进一步信息
    param
        position_id(list): 从数据库中获取的p_id
    return
        descriptions(list): 进一步爬取的详细信息
    """
    descriptions = list()
    print(len(position_id))
    i = 0
    for p_id in position_id:
        url = 'https://m.lagou.com/jobs/{}.html'.format(p_id)
        req = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if req.status_code == 200:
            html_code = req.text
            '''
                <div class="content">
                    <p>注意：工作地点在杭州</p>
                    <p><br></p>
                    <p>职位描述：</p>
                    <p>...</p>
                    ...
                    <p>...</p>
                    <p><br></p>
                    <p>岗位要求：</p>
                    <p>...</p>
                    ...
                    <p>...</p>
                    <p><br></p>
                    </div>
            </div>
            '''
            soup = BeautifulSoup(html_code, 'html5lib')
            # job_bt = soup.findAll('dd',{'class': 'job_bt'})[0]
            # doms = job_bt.findAll('div')[0]
            # doms = doms.findAll('p')
            # data = [item.get_text() for item in doms]
            # print(p_id)
            jd = soup.find_all('div', class_='content')[0].get_text().strip().replace('\n', '').replace('&nbps;', '').replace('\'', '\\\'')
            # print(jd)
            descriptions.append(jd)
            print(i)
            i += 1
        else:
            print(req.status_code)
        time.sleep(2)
    return descriptions


def save_mysql(db, cursor, position_id, descriptions):
    """
    将获取到的详细信息存入到mysql
    """
    sql = '''
    UPDATE lagou_crawl.posiition_info
    SET job_description='%s'
    WHERE positionId='%s'
    '''
    for i in range(len(descriptions)):
        update_sql = sql % (descriptions[i], position_id[i])
        print(update_sql)
        cursor.execute(update_sql)
        db.commit()


if __name__ == '__main__':

    db = pymysql.connect('localhost', 'root', '******', 'lagou_crawl', charset='utf8')
    cursor = db.cursor()

    position_id = get_position_id(cursor)
    print(position_id)
    descriptions = get_descriptions(position_id)
    # print(descriptions)
    print('爬取完毕')
    
    save_mysql(db, cursor, position_id, descriptions)
    print('存储完毕')
    cursor.close()
    db.close()
