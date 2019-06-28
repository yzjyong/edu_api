import pymysql
from pymysql.cursors import DictCursor
from logger import api_logger


DB_CONFIG = {
    "host":"localhost",
    "port":3306,
    "user":"eduadmin",
    "password":"edu7654",
    "db":"edu_api_db",
    "charset":"utf8"
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

        return True # 异常不会继续向外抛出


class BaseDao():
    def __init__(self):
        self.db = DB()

    def save(self,table_name,**values):
        sql = 'insert into %s(%s) values(%s)' % \
              (table_name,
               ','.join(values.keys()),
               ','.join(['%%(%s)s' % key for key in values.keys()])
               )
        success = False
        with self.db as c:
            c.execute(sql,args=values)
            api_logger.info('%s ok!' % sql)
            success = True
        return success

    def update(self, table_name, key,value, where=None, args=None):
        sql = "update {} set {}='{}' where {}='{}' ".format(
            table_name, key,value, where, args
        )
        succuss = False
        with self.db as c:
            print(sql)
            c.execute(sql)
            api_logger.info('%s ok!' % sql)
            succuss = True
        return succuss

    def delete(self,table_name,by_id):
        pass

    def list(self,table_name,*fileds,
             where=None,args=None,page=1,page_size=20):
        if not where:
            sql = "select {} from {} limit {},{}".format\
                (','.join(*fileds),table_name,(page-1)*page_size,page_size)
        else:
            sql = "select {} from {} where {}={} limit {},{}".format\
                (','.join(*fileds),table_name,where,args,(page-1)*page_size,page_size)
        with self.db as c:
            c.execute(sql)
            result = c.fetchall()
            api_logger.info('%s ok!' % sql)
            return result

    def count(self,table_name):
        pass

    def query(self,sql,*args):
        with self.db as c:
            c.execute(sql,args=args)
            data = c.fetchall()
            if data:
                data = list(data)
        return data

if __name__ == '__main__':
    # user_data = {'u_phone': 18729541663,'is_active': True,'is_delete': False,'u_pname':'wx','note':'1213'}
    # print(BaseDao().save('users', **user_data))
    print(BaseDao().update('users','u_auth_string','66bdfc2356d645deae67ff42993aa49d','u_phone','18729541663'))