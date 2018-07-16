"""
    @Time: 2018/7/10 20:38
    @Author: qingyaocui
"""
import pymysql


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
                             port=self.port,
                             charset='utf8')

        return connection

    def add(self, data):
        '''
        向数据库中插入数据
        :param data: 字典格式 "字段名称" :"字段值"
        :return:
        '''
        # 重复检测，如果要插入的数据全部重复则认为重复,直接return
        if len(self.find_job_id_by_jobmsg(data)) != 0:
            print('添加失败，招聘条目重复!')
            return
        # 构造sql
        left = 'INSERT INTO jobinfomation('
        right = ' VALUES ('
        l = len(data)
        count = 0
        for key in data:
            if count+1 == l:
                left += key + ')'
                right += data[key] + ')'
            else:
                left += key + ','
                right += data[key] + ','
                count+=1
        sql = left + right

        # 执行sql语句
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                print("插入数据成功！")
        finally:
            self.close_db(conn)

    def update(self, job_id, data):
        '''
        更新数据库
        :param job_id:要更改的招聘id
        :param data:更改的数据
        :return:
        '''
        sql = 'UPDATE jobinfomation SET '

        l = len(data)
        count = 0
        for key in data:
            if count + 1 == l:
                sql += key + '=' + data[key]
            else:
                sql += key + '=' + data[key] + ','
                count += 1
        sql += ' WHERE job_id=%d' % (job_id)

        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                print("更新数据成功！")
        finally:
            self.close_db(conn)

    def find_job_id_by_jobmsg(self, data):
        '''
        查询某条符合条件的招聘信息的job_id
        :return: job_id
        '''

        sql = 'SELECT job_id FROM jobinfomation WHERE '

        l = len(data)
        count = 0
        for key in data:
            if count + 1 == l:
                sql += key + '=' + data[key]
            else:
                sql += key + '=' + data[key] + ' AND '
                count += 1
        # print(sql)
        conn = self.get_connection()
        results = None
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            self.close_db(conn)
        return results


    def findall(self):
        '''
        查询jobinfomation表中的前5条信息
        :return: jobinfomation表中的前5条数据
        '''
        sql = "SELECT job_id,com_name,com_type,com_size,busi_type,com_info,com_loc_simple,com_loc_detail,job_title,"+\
              "salary,release_time,num_of_recruits,academic_require,treatment,job_info FROM jobinfomation "
        conn = self.get_connection()
        results = None
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fe

        finally:
            self.close_db(conn)


    def find_fields(self, fields):
        '''
        查询某一个字段的所有信息
        :param field: 某一个字段
        :return:
        '''

        if fields:
            if isinstance(fields,list) or isinstance(fields, tuple):

                if len(fields) > 1:
                    sql = 'SELECT '+','.join(fields)+' FROM jobinfomation'
                elif len(fields) == 1:
                    sql = 'SELECT' + fields[0] + ' FROM jobinfomation'
                else:
                    return None
            else:
                return None
        else:
            return None

        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            self.close_db(conn)

        return results

    def close_db(self, conn):
        '''
        关闭数据库连接，释放资源
        :param conn: 数据库连接对象
        :return:
        '''
        if conn:
            conn.close()

