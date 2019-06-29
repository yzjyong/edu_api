import pymysql
from pymysql.cursors import DictCursor
from logger import api_logger

DB_CONFIG = {
    "host": "121.199.63.71",
    "port": 3306,
    "user": "eduadmin",
    "password": "eduadmin",
    "db": "edu_api_db",
    "charset": "utf8"
}


class DB:
    def __init__(self):
        self.conn = pymysql.Connect(**DB_CONFIG)

    def __enter__(self):
        if self.conn is None:
            self.conn = pymysql.Connect(**DB_CONFIG)
        return self.conn.cursor(cursor=DictCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            api_logger.error(exc_val)
            self.conn.rollback()
<<<<<<< HEAD

        return True  # 异常不会继续向外抛出
=======
        return True # 异常不会继续向外抛出
>>>>>>> 1773eba99439a1822000f4e07720f44636620202


class BaseDao():
    def __init__(self):
        self.db = DB()

<<<<<<< HEAD
    def save(self, table_name, **values):
=======
    # 增
    def save(self,table_name,**values):
>>>>>>> 1773eba99439a1822000f4e07720f44636620202
        sql = 'insert into %s(%s) values(%s)' % \
              (table_name,
               ','.join(values.keys()),
               ','.join(['%%(%s)s' % key for key in values.keys()])
               )
        success = False
        with self.db as c:
            c.execute(sql, args=values)
            api_logger.info('%s ok!' % sql)
            success = True
        return success

<<<<<<< HEAD
    def update(self, table_name, key, value, where=None, args=None):
=======
    # 删
    def delete(self, table_name, where=None, args=None):
        sql = "delete from {} where {}='{}'".format(table_name, where, args)
        success = False
        with self.db as c:
            c.execute(sql)
            api_logger.info('%s ok!' % sql)
            success = True
        return success

    # 改
    def update(self, table_name, key,value, where=None, args=None):
>>>>>>> 1773eba99439a1822000f4e07720f44636620202
        sql = "update {} set {}='{}' where {}='{}' ".format(
            table_name, key, value, where, args
        )
        succuss = False
        with self.db as c:
            c.execute(sql)
            api_logger.info('%s ok!' % sql)
            succuss = True
        return succuss

<<<<<<< HEAD
    def delete(self, table_name, by_id):
        pass

    def list(self, table_name, *fileds,
             where=None, args=None, page=1, page_size=20):
        if not where:
            sql = "select {} from {} limit {},{}".format \
                (','.join(*fileds), table_name, (page - 1) * page_size, page_size)
        else:
            sql = "select {} from {} where {}={} limit {},{}".format \
                (','.join(*fileds), table_name, where, args, (page - 1) * page_size, page_size)
=======
    # 查
    def list(self,table_name,*fileds,where=None,args=None,page=1,page_size=20):
        if not where: # 无条件查询
            sql = "select {} from {} limit {},{}".format\
                (','.join(*fileds),table_name,(page-1)*page_size,page_size)
        else:   # 条件查询
            sql = "select {} from {} where {}={} limit {},{}".format\
                (','.join(*fileds),table_name,where,args,(page-1)*page_size,page_size)
>>>>>>> 1773eba99439a1822000f4e07720f44636620202
        print(sql)
        with self.db as c:
            c.execute(sql)
            result = c.fetchall()
            api_logger.info('%s ok!' % sql)
            return result

<<<<<<< HEAD
    def count(self, first_table_name, *fileds, arg, alias, second_table_name=None, b_con=None, a_con=None, b_arg=None,
              a_arg=None, args):
        if not second_table_name:
            sql = "select {}, count({}) as {} from {} group by {}".format \
                (','.join(*fileds), arg, alias, first_table_name, args)
        else:
            sql = "select {}, count({}) as {} from {} join {} on {}={} and {}={} group by {}".format \
                (','.join(*fileds), arg, alias, first_table_name, second_table_name, b_con, a_con, b_arg, a_arg, args)
        with self.db as c:
            c.execute(sql)
            data = c.fetchall()
            api_logger.info('%s ok!' % sql)
            if data:
                data = list(data)
        return data

    def query(self, sql, *args):
=======
    # sql语句执行
    def query(self,sql,*args):
>>>>>>> 1773eba99439a1822000f4e07720f44636620202
        with self.db as c:
            c.execute(sql, args=args)
            data = c.fetchall()
            if data:
                data = list(data)
        return data

<<<<<<< HEAD
=======
    # 计数
    def count(self,table_name):
        pass
>>>>>>> 1773eba99439a1822000f4e07720f44636620202

if __name__ == '__main__':
    print(BaseDao().list('teachers', '*'))
