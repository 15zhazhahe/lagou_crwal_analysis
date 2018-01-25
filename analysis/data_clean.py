"""
对一些数据进行清洗,便于分析
获取需要分析的数据
"""
import pymysql
import pandas as pd

def clean_salary(db, cursor):
    """
    对工资进行清理,增加三列(min, max, avg)
    alter table lagou_crawl.position_info add(
        min_salary	float(10),
        max_salary	float(10),
        avg_salary	float(10)
    );
    """
    sql = '''
    select positionId,salary from lagou_crawl.position_info
    '''
    id_salary = dict()
    cursor.execute(sql)
    for data in cursor.fetchall():
        id_salary[data[0]] = data[1]
    # print(id_salary)
    sql = '''
    UPDATE lagou_crawl.position_info
    SET %s=%.2f
    WHERE positionId=%s
    '''
    for key in id_salary.keys():
        salary = id_salary[key]
        salary = salary.split('-')
        # print(salary)
        min_salary = float(salary[0][:-1])
        max_salary = float(salary[1][:-1])
        avg_salary = (min_salary+max_salary)/2.0
        print(min_salary, max_salary, avg_salary)
        print(sql % ('min_salary', min_salary, key))
        cursor.execute(sql % ('min_salary', min_salary, key))
        cursor.execute(sql % ('max_salary', max_salary, key))
        cursor.execute(sql % ('avg_salary', avg_salary, key))
    db.commit()


def clean_companyLabelList(db, cursor):
    '''
    变成以逗号隔开
    '''
    sql = '''
    select positionId,companyLabelList from lagou_crawl.position_info
    '''
    id_label = dict()
    cursor.execute(sql)
    for data in cursor.fetchall():
        id_label[data[0]] = data[1]
    sql = '''
    UPDATE lagou_crawl.position_info
    SET companyLabelList='%s'
    WHERE positionId='%s'
    '''
    for key in id_label.keys():
        label = id_label[key]
        label = label.replace('-', ',')
        if len(label) < 3:
            label = 'null'
        print(sql % (label, key))
        cursor.execute(sql % (label, key))
    db.commit()


def clean_industryField(db, cursor):
    '''
    改变一下数据的表示形式,有些属于跨行业领域,缩小范围
    '''
    sql = '''
    select positionId,industryField from lagou_crawl.position_info
    '''
    id_industry = dict()
    cursor.execute(sql)
    for data in cursor.fetchall():
        id_industry[data[0]] = data[1]
    sql = '''
    UPDATE lagou_crawl.position_info
    SET industryField='%s'
    WHERE positionId='%s'
    '''
    for key in id_industry.keys():
        industry = id_industry[key]
        if industry.find('电子商务') != -1:
            industry = '电子商务'
        elif industry.find('金融') != -1:
            industry = '金融'
        elif industry.find('企业服务') != -1:
            industry = '企业服务'
        elif industry.find('教育') != -1:
            industry = '教育'
        elif industry.find('文化娱乐') != -1:
            industry = '文化娱乐'
        elif industry.find('游戏') != -1:
            industry = '游戏'
        elif industry.find('O2O') != -1:
            industry = 'O2O'
        elif industry.find('硬件') != -1:
            industry = '硬件'
        elif industry.find('社交网络') != -1:
            industry = '社交网络'
        elif industry.find('旅游') != -1:
            industry = '旅游'
        elif industry.find('医疗健康') != -1:
            industry = '医疗健康'
        elif industry.find('生活服务') != -1:
            industry = '生活服务'
        elif industry.find('信息安全') != -1:
            industry = '信息安全'
        elif industry.find('数据服务') != -1:
            industry = '数据服务'
        elif industry.find('广告营销') != -1:
            industry = '广告营销'
        elif industry.find('分类信息') != -1:
            industry = '分类信息'
        elif industry.find('招聘') != -1:
            industry = '招聘'
        elif industry.find('移动互联网') != -1:
            industry = '移动互联网'
        else:
            industry = '其他'
        print(sql % (industry, key))
        cursor.execute(sql % (industry, key))
    db.commit()


def get_data(db):
    sql = '''
    select positionName,companyShortName,
    min_salary,max_salary,avg_salary,
    companyLabelList,job_description,industryField,companySize,
    city,education,workyear,firstType
    from lagou_crawl.position_info;
    '''
    data = pd.read_sql(sql, db)
    data['count'] = 1
    return data


db = pymysql.connect('localhost', 'root', 'lvoe07', 'lagou_crawl', charset='utf8')
cursor = db.cursor()

# clean_salary(db, cursor)
# clean_companyLabelList(db, cursor)
# clean_industryField(db, cursor)
data = get_data(db)
# print(data)

cursor.close()
db.close()
