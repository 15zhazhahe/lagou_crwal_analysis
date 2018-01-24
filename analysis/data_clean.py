"""
对一些数据进行清洗,便于分析
"""
import pymysql


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


db = pymysql.connect('localhost', 'root', '*****', 'lagou_crawl', charset='utf8')
cursor = db.cursor()

# clean_salary(db, cursor)
clean_companyLabelList(db, cursor)

cursor.close()
db.close()
