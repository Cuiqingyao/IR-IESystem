# IR-IESystem
Information Retrieval &amp; Information Extraction System

## 程序结构

- conf 存放数据库和爬虫的相关配置文件
- Crawler--spider.py 爬虫程序
- db--DBHelper.py 操作数据库
    --jobs.sql 包含数据库结构和数据的SQL脚本
- mysite web程序，提供浏览器访问页面
- screenshot 存放中间结果截图，项目运行截图
- utils 工具函数库
- word_cut 分词与统计相关程序

## 相关依赖库
```

- pymysql
- requests
- BeautifulSoup
- django


```

