-- 创建数据库lagou_crawl
create database lagou_crawl;

-- 根据excel创建表
create table posiition_info(
	positionId 			int primary key,
    positionName		varchar(50),
    education			varchar(50),
    salary				varchar(50),
    workyear			varchar(50),
    firstType			varchar(50),
    secondType			varchar(50),
	positionLables		varchar(50),
    companyLabelList 	varchar(50),
    companyId			int,
    companyShortName	varchar(50),
    companyFullName		varchar(50),
    industryField		varchar(50),
    companySize			varchar(50),
    financeStage		varchar(50),
    city				varchar(50),
    latitude			double,
    longitude			double
)default charset=utf8;

-- 加多一列表示职位的职责和要求
alter table lagou_crawl.position_info add column job_description text;
