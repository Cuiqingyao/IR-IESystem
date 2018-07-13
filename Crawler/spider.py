"""
    @Time: 2018/7/11 16:57
    @Author: qingyaocui
"""

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from conf.spider_conf import *
from conf.dbconf import *
from db.db_helper import DBHepler
from multiprocessing import Pool
from multiprocessing import Lock
from utils.util import clean_str
import re
import time

db_helper = DBHepler(localhost=LOCALHOST, username=USERNAME, password=PASSWORD, port=PORT, db_name=DATABASE_NAME)
lock = Lock()

def get_one_page(url):
    try:

        response = requests.get(url, headers=HEADERS)
        # 由于 51job 上的网页编码格式为gbk 或者 gb2312 所以这里修改response对象的编码格式
        response.encoding = 'gbk'
        if response:
            if response.status_code == 200:
                return response.text
        return None
    except RequestException as e:
        print('请求出现异常！')
        return None

def parse_job_page(html):
    '''
    通过requests + 正则表达式来完成招聘条目解析
    :param html: 页面源码
    :return:
    '''

    pattern = re.compile(JOB_PATTERN, re.S)
    results = re.findall(pattern, html)
    # 多个结果构造生成器，可以节省内存
    for result in results:
        yield {
            'job_url' : '\"' + result[0] +'\"',
            'job_title' : '\"' + result[1].strip() + '\"',
            'com_name' : '\"' + result[2].strip() + '\"',
            'com_url' : '\"' + result[3] + '\"',
            'com_loc_simple' : '\"' + result[4] + '\"',
            'salary' : '\"' + result[5] + '\"',
            'release_time' : '\"' + '2018-' + result[6] + '\"'
        }

def parse_com_page(html):
    '''
    通过BeautifulSoup + re来完成职位详情页面的解析
    :param html: 页面源代码
    :return:
    '''
    data_dict = {}
    soup = BeautifulSoup(html, 'lxml')
    # 解析com_type, com_size, busi_type字段，加入data_dict字典
    com_msg = soup.select('.cn .msg')
    if len(com_msg) != 0:
        contents = com_msg[0].get_text().strip().split('|')
        if len(contents) == 3:
            data_dict['com_type'] = '\"' + contents[0].strip() + '\"'
            data_dict['com_size'] = '\"' + contents[1].strip() + '\"'
            data_dict['busi_type'] = '\"' + contents[2].strip() + '\"'
        else:
            data_dict['com_type'] = '\"' + '<unknow>' + '\"'
            data_dict['com_size'] = '\"' + '<unknow>' + '\"'
            data_dict['busi_type'] = '\"' + '<unknow>' + '\"'
    else:
        data_dict['com_type'] = '\"' + '<unknow>' + '\"'
        data_dict['com_size'] = '\"' + '<unknow>' + '\"'
        data_dict['busi_type'] = '\"' + '<unknow>' + '\"'

    # 解析 num_of_recruits, academic_require字段，加入data_dict字典
    require_msg = []
    for item in soup.select('.sp4'):
        require_msg.append(item.text)
    data_dict['academic_require'] = '\"' + require_msg[1] + '\"'
    data_dict['num_of_recruits'] = '\"' + require_msg[2] + '\"'

    # 解析 treatment字段，加入data_dict字典
    data_dict['treatment'] = '暂无'
    treatments_msg = soup.select('.t2')
    if treatments_msg:
        data_dict['treatment'] = ''
        for item in treatments_msg:
            data_dict['treatment'] += item.text.strip()
    data_dict['treatment'] = '\"' + data_dict['treatment'] + '\"'

    # 解析job_info, com_info, com_loc_detail字段，加入data_dict字典
    all_info = soup.select('.tBorderTop_box')
    #print(len(all_info))
    try:
        data_dict['job_info'] = '\"' + clean_str(re.sub('\n+', '', all_info[1].text)[4:]) + '\"'
        data_dict['com_loc_detail'] = '\"' + clean_str(all_info[2].select('.fp')[0].text) + '\"'
        #print(all_info[3].select('.tmsg'))
        data_dict['com_info'] = '\"' + clean_str(all_info[3].select('.tmsg')[0].text.strip()) + '\"'
    except Exception as e:
        data_dict['job_info'] = '\"' + '<unknow>' + '\"'
        data_dict['com_loc_detail'] = '\"' + '<unknow>' + '\"'
        data_dict['com_info'] = '\"' + '<unknow>' + '\"'

    return data_dict



def main(academic):
    '''
    爬虫程序入口
    :return:
    '''

    # part_1 : 爬取招聘条目信息， 部分字段残缺，需进入具体的url进行不全
    print("招聘条目信息开始爬取-----")
    # for key in ACADEMIC_REQUIRE_DICT:
    print("["+ACADEMIC[academic]+"]招聘爬取任务完成度：")
    base_url = ACADEMIC_REQUIRE_DICT[academic]
    for i in range(1, DATA_CAPACITY[academic]+1):

        url = base_url.replace('1.html', str(i)+'.html')
        html = get_one_page(url)

        # t = random.randint(10,20)
        # time.sleep(t)
        for item in parse_job_page(html):
            db_helper.add(item)

        print("[%s]已经爬取： %d" % (ACADEMIC[academic], i)+"页")

    # part_2 : 补全剩余字段
    lock.acquire()
    print("招聘条目详情页开始爬取-----")
    id_and_urls = db_helper.find_fields(fields=['job_id', 'job_url'])
    if id_and_urls:
        l = len(id_and_urls)
        for index, id_and_url in enumerate(id_and_urls):
            if index % 100 == 0 or (index+1) == l:
                print("详情页爬取完成度：")
                print("已经爬取: %d条, 共%d" % (index, l))
            job_id = id_and_url[0]
            url = id_and_url[1]
            html = get_one_page(url)
            # t = random.randint(5, 10)
            # time.sleep(t)
            data = parse_com_page(html)
            db_helper.update(job_id, data)
    else:
        print("id_and_urls 未找到!")
    lock.release()
if __name__ == '__main__':
    start = time.time()
    pool = Pool(3)
    pool.map(main, list(ACADEMIC_REQUIRE_DICT.keys()))
    end = time.time()
    print("总时长：%f" % (end-start))


