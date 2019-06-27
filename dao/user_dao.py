from dao import BaseDao
from libs.crypt import check_password, make_password
from logger import api_logger
from services.sms_check import check_sms


class UserDao(BaseDao):

    def save(self,**values):
        api_logger.info('db replace users:<%s>' % values['u_phone'])
        return super(UserDao,self).save('users',**values)

    def list(self,*fileds,where=None, args=None):
        api_logger.info('db select users')
        return super(UserDao,self).list('users','*',where=where,args=args)

    def user_update(self,key,value, where, args):
        api_logger.info('db update users')
        value = make_password(value) if key == 'u_auth_string' else value
        return super(UserDao, self).update('users', key,value, where, args)

    def check_login_phone(self,u_phone):
        # 检查用户名是否已存在
        result = self.query('select id as cnt from users where u_phone=%s',u_phone)
        return bool(result)

    def pwdlogin(self,phone,auth_string):
        sql = "select id,u_auth_string from users where u_phone=%s"
        user_data = self.query(sql, phone)
        id, auth_str = (user_data[0].get('id'),
                        user_data[0].get('u_auth_string'))
        if check_password(auth_string, auth_str):
            user_profile = self.get_profile(id)
            if user_profile is None:
                return {'u_phone':phone}
            return user_profile
        api_logger.warn('用户 %s 的口令不正确' % phone)
        return {'code':'303','msg':'用户口令不正确'}

    def get_profile(self,id):
        # 获取用户详细信息
        sql = 'select * from users where id=%s'
        user_profile = self.query(sql,id)
        if user_profile:
            return user_profile[0]

    def msglogin(self,u_phone,msg_code):
        sql = 'select id from users where u_phone=%s'
        user_data = self.query(sql, u_phone)
        id = user_data[0].get('id')
        res = check_sms(u_phone, msg_code)
        if not res:
            # 验证成功
            user_profile = self.get_profile(id)
            if user_profile is None:
                return {'u_phone': u_phone}
            return user_profile
        return res

if __name__ == '__main__':
    u_dao = UserDao()
    value = make_password('qwe')
    print(value)
    u_dao.user_update('u_auth_string','66bdfc2356d645deae67ff42993aa49d','u_phone','18729541663')