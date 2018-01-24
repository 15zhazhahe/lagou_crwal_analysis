-- 观察数据,处理需要的清洗的数据
select * from lagou_crawl.position_info;
-- 处理工资(salary)
select count(salary) from lagou_crawl.position_info
where salary like '%k-%k';		-- 450
-- 全部都为 min k-max k的形式,故增加三列(最低,最高,平均)
alter table lagou_crawl.position_info add(
	min_salary	float(10),
    max_salary	float(10),
    avg_salary	float(10)
);
select positionId,companyLabelList from lagou_crawl.position_info;

select count(companyLabelList) from lagou_crawl.position_info
where length(companyLabelList) < 3
group by companyLabelList;

SELECT positionName,companyShortName,min_salary,max_salary,avg_salary,
companyLabelList,job_description,industryField,companySize,
city,education,workyear,firstType
from lagou_crawl.position_info;