import pymysql
from pymysql.cursors import DictCursor
from logger import api_logger

DB_CONFIG = {
    "host": "121.199.63.71",
    "port": 3306,
    "user": "eduadmin",
    "password": "edu7654",
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

        return True  # 异常不会继续向外抛出


class BaseDao():
    def __init__(self):
        self.db = DB()

    # 增
    def save(self, table_name, **values):
        sql = 'insert into %s(%s) values(%s)' % \
              (table_name,
               ','.join(values.keys()),
               ','.join(['%%(%s)s' % key for key in values.keys()])
               )
        print("sql",sql)
        success = False
        with self.db as c:

            c.execute(sql, args=values)
            api_logger.info('%s ok!' % sql)
            success = True
        return success

    # 删
    def delete(self, table_name, where=None, args=None):
        sql = "delete from {} where {}='{}'".format(table_name, where, args)
        success = False
        with self.db as c:
            c.execute(sql)
            print("sql11",sql)
            api_logger.info('%s ok!' % sql)
            success = True
        return success

    # 改
    def update(self, table_name, key, value, where=None, args=None):
        sql = "update {} set {}='{}' where {}='{}' ".format(
            table_name, key, value, where, args
        )
        succuss = False
        with self.db as c:
            c.execute(sql)
            api_logger.info('%s ok!' % sql)
            succuss = True
        return succuss

    # 查
    def list(self, table_name, *fileds, where=None, args=None, page=1, page_size=20):
        if not where:  # 无条件查询
            sql = "select {} from {} limit {},{}".format \
                (','.join(*fileds), table_name, (page - 1) * page_size, page_size)
        else:  # 条件查询
            sql = "select {} from {} where {}={} limit {},{}".format \
                (','.join(*fileds), table_name, where, args, (page - 1) * page_size, page_size)
        print(sql)
        with self.db as c:
            c.execute(sql)
            print(sql)
            result = c.fetchall()
            api_logger.info('%s ok!' % sql)
            return result

    # sql语句执行
    def query(self, sql, *args):
        with self.db as c:
            c.execute(sql, args=args)
            print('====',sql)
            data = c.fetchall()
            if data:
                data = list(data)
            return data

    # 计数
    def count(self, first_table_name, *fields, arg, alias, second_table_name=None, b_con=None, a_con=None,
              b_arg=None,
              a_arg=None, args):
        if not second_table_name:
            sql = "select {}, count({}) as {} from {} group by {}".format \
                (','.join(*fields), arg, alias, first_table_name, args)
        else:
            sql = "select {}, count({}) as {} from {} join {} on {}={} and {}={} group by {}".format \
                (','.join(*fields), arg, alias, first_table_name, second_table_name, b_con, a_con, b_arg, a_arg,
                 args)
        with self.db as c:
            c.execute(sql)
            data = c.fetchall()
            api_logger.info('%s ok!' % sql)
            if data:
                data = list(data)
        return data


if __name__ == '__main__':
    print(BaseDao().list('teachers', '*'))
