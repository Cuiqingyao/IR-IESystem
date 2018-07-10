"""
    @Time: 2018/7/10 20:38
    @Author: qingyaocui
"""
import pymysql
from conf.dbconf import *

class DBHepler:
    '''
    DBHepler类：用于封装数据库连接，增删改查等操作
    数据库连接信息从conf/dbconf.py中的配置项获得
    '''
    def __init__(self, localhost, username, password, port, db_name):
        '''
        初始化数据库连接
        :param localhost: 主机地址
        :param username: 用户名
        :param password: 密码
        :param port: 端口
        :param db_name: 数据库名称
        '''
        self.localhost = localhost
        self.username = username
        self.password = password
        self.port = port
        self.db_name = db_name


    def __str__(self):
        '''
        打印DBHepler对象信息（相当于java中的toString方法）
        :return: 数据库连接信息
        '''
        return "数据库连接信息：\
               主机地址：%s\n\
               用户名：%s\
               密码：%s\n\
               端口：%s\
               数据库名称：%s" % (self.localhost, self.username, self.password, self.port, self.db_name)

    def get_connection(self):
        '''
        返回数据库连接对象
        :return: 数据库连接对象
        '''
        connection = pymysql.connect(host=self.localhost,
                             user=self.username,
                             password=self.password,
                             db=self.db_name,
                             port=self.port)

        return connection

    def add(self, data):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def findall(self):
        '''
        查询jobinfomation表中的前5条信息
        :return: jobinfomation表中的前5条数据
        '''
        sql = "SELECT job_id,com_name,com_type,com_size,busi_type,com_info,com_loc_simple,com_loc_detail,job_title,"+\
              "salary,release_time,num_of_recruits,academic_require,treatment,job_info FROM jobinfomation LIMIT 5"
        conn = self.get_connection()
        results = None
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            self.close_db(conn)
        return results


    def find_by_id(self, id):
        pass

    def close_db(self, conn):
        '''
        关闭数据库连接，释放资源
        :param conn: 数据库连接对象
        :return:
        '''
        if conn:
            conn.close()



# if __name__ == '__main__':
#     dbhelper = DBHepler(LOCALHOST, USERNAME, PASSWORD, PORT, DATABASE_NAME)
#     print(dbhelper)
#     results = dbhelper.findall()
#     if results:
#         for result in results:
#             print(result)