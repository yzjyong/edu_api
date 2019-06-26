from dao import BaseDao
from libs.crypt import check_password, make_password
from logger import api_logger
from services.sms_check import check_sms


class UserDao(BaseDao):

    def save(self,table_name,**values):
        api_logger.info('db replace users:<%s>' % values['u_phone'])
        values['u_auth_string'] = make_password(values['u_auth_string'])
        return super(UserDao,self).save('users',**values)

    def list(self, table_name, *fileds,where=None, args=None):
        api_logger.info('db select users')
        return super(UserDao,self).list('users','*',where=where,args=args)

    def check_login_phone(self,u_phone):
        # 检查用户名是否已存在
        result = self.query('select id as cnt from users where u_phone=%s',u_phone)
        return bool(result)

    def login(self,phone,auth_string):
        sql = "select id,u_auth_string from users where u_phone=%s"
        user_data = self.query(sql, phone)
        if user_data:
            id, auth_str = (user_data[0].get('id'),
                            user_data[0].get('u_auth_string'))
            if check_password(auth_string, auth_str):
                user_profile = self.get_profile(id)
                if user_profile is None:
                    return {
                        'user_id':id,
                        'u_phone':phone
                    }
                return user_profile
            api_logger.warn('用户 %s 的口令不正确' % phone)
            raise Exception('用户 %s 的口令不正确' % phone)
        else:
            api_logger.warn('查无此用户 %s' % phone)
            raise Exception('查无此用户 %s' % phone)

    def get_profile(self,id):
        # 获取用户详细信息
        sql = 'select * from users where id=%s'
        user_profile = self.query(sql,id)
        if user_profile:
            return user_profile[0]

    def msglogin(self,u_phone,msg_code):
        sql = 'select id from users where u_phone=%s'
        user_data = self.query(sql, u_phone)
        if user_data:
            id = user_data[0].get('id')
            if check_sms(u_phone,msg_code):
                # 验证成功
                user_profile = self.get_profile(id)
                if user_profile is None:
                    return {
                        'user_id': id,
                        'u_phone': u_phone
                    }
                return user_profile
            api_logger.warn('用户 %s 验证码不正确' % u_phone)
            raise Exception('用户 %s 验证码不正确' % u_phone)
        else:
            api_logger.warn('查无此用户 %s' % u_phone)
            raise Exception('查无此用户 %s' % u_phone)

if __name__ == '__main__':
    u_dao = UserDao()
    u_dao.login('18729541669', 'msg', auth_string=None, msg_code='123456')