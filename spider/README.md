# 爬取拉勾网的数据[requests, BeautifulSoup]

采用requests爬取拉勾网动态与静态内容,获取相关岗位的行业分布,地域分布,技术要求等相关内容

---

# 实现过程
先提交表单访问拉勾网,获得返回的json数据,将数据存入mysql中.

再根据对应职位id进一步访问拉勾网,通过BeautifulSoup爬取静态网页中需要的内容

# 代码解析

**`crawl_brief.py`**  第一次爬取,得到json数据,存入excel中

**`crwal_description.py`** 拿出positionId,进一步爬取更加详细的信息

**`save_mysql.py`** 将excel的数据存入mysql中
    