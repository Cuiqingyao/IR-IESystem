"""
    @Time: 2018/7/13 14:01
    @Author: qingyaocui
"""

import pymysql
from utils.util import seg_list, clean
from conf.dbconf import *
stopwords_path = './stopwords.txt'
'''
分词模块所做的工作分为3个步骤：进行数据清洗，字段拼接，文档分词
'''
conn = pymysql.connect(host=LOCALHOST,
                       user=USERNAME,
                       password=PASSWORD,
                       port=PORT,
                       db=DATABASE_NAME,
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)

'''
step 1: 清洗数据,删除job_info字段或com_info字段为<unknow>标识的字段的招聘条目
'''

clean_data_sql = 'DELETE FROM jobinfomation WHERE job_info="<unknow>" or com_info="<unknow>"'
cursor = conn.cursor()
cursor.execute(clean_data_sql)
conn.commit()
cursor.close()

# 从数据库中查询出部分字段的信息，用于拼接生成文档

sql = 'SELECT job_id, com_name, busi_type, com_info, com_loc_simple, com_loc_detail, job_title, academic_require, treatment, job_info FROM jobinfomation'
cursor = conn.cursor()
cursor.execute(sql)


while 1:
    jobs = cursor.fetchone()
    if jobs:

        '''
        step 2: 将数据库中各个字段中的某些字段拼接生成文本contents，存入./data/contents/目录下
        文件命名方式为：{job_id}_contents.txt
        '''
        with open('./data/contents/contents.txt', 'a', encoding='utf-8') as f:
            contents = '%d\t%s%s%s%s' % (jobs['job_id'],
                                         clean(jobs['job_title'].strip()),
                                         clean(jobs['job_info'].strip()),
                                         clean(jobs['busi_type'].strip()),
                                         clean(jobs['com_info'].strip())
                                         )
            f.write(contents + '\n')
    else:
        break

'''
 step 3: 将./data/contents/目录下的每个文件进行分词操作，生成分词结果，存入./data/cuts/目录下
 文件命名方式为：{job_id}_cuts.txt

 note: 分词使用的函数是utils/util.py 文件中的seg_list函数
'''
with open('./data/contents/contents.txt', 'r', encoding='utf-8') as f1:
    for line in f1.readlines():
        # print(line)
        id_sentence = line.split('\t')
        with open('./data/cuts/%s_cuts.txt'%(id_sentence[0]), 'w', encoding='utf-8') as f2:

            s = '/'.join(seg_list(sentence=id_sentence[1],
                                   isstop=True,
                                   stopwords=stopwords_path))
            f2.write(s)





