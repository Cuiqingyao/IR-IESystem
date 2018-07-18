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
安装命令 pip3 install 依赖库名称
- pymysql
- requests
- BeautifulSoup
- django


```
## 如何运行

1.首先在本地配置好python3.6环境，安装相关依赖库。
1.接着需要在mysql数据库上运行jobs.sql脚本。
2.(选做)在确保网络平稳的状态下，运行Clawler--spider.py文件对51job网站上的招聘信息进行爬取并存储到mysql数据库中，因为在jobs.sql中已经将数据的插入命令写好，所以这一步选做(注意：因为爬虫程序爬取过程较慢，如果只是想看项目的演示过程，则可跳过这一步)。
3.进入mysite目录下,运行```python manage.py runserver 8080```命令，服务器将自行启动。
4.打开浏览器（建议使用Chrome），在地址栏输入```127.0.0.1:8080```，回车即可访问项目首页。