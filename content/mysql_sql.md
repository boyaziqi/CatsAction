Title: Mysql SQL之group by
Date: 2017-04-01
category: mysql
tags: group by, sql

group by用来对数据进行分组，如果不止一条数据，则会返回第一条。

### 1：group by语法
```SQL
SELECT * FROM `table`
WHERE `id`=12
GROUP BY `id`
```
