from datetime import datetime
from dao import BaseDao
from libs.crypt import check_password, make_password
from logger import api_logger
from services.sms_check import check_sms


class UserDao(BaseDao):

    # 保存用户信息
    def save(self,**values):
        api_logger.info('db insert users:<%s>' % values['u_phone'])
        return super(UserDao,self).save('users',**values)

    # 查询用户信息
    def user_list(self,where, args):
        api_logger.info('db select users')
        return super(UserDao,self).list('users','*',where=where,args=args)

    # 更新用户数据
    def user_update(self,key,value, where, args):
        api_logger.info('db update users')
        value = make_password(value) if key == 'u_auth_string' else value   # 更新字段是密码时，加密
        return super(UserDao, self).update('users', key,value, where, args)

    # 检查用户名是否已存在：返回布尔值
    def check_login_phone(self,u_phone):
        result = self.query('select id as cnt from users where u_phone=%s',u_phone)
        return bool(result)

    # 获取用户详细信息
    def get_profile(self,id):
        sql = 'select * from users where id=%s'
        user_profile = self.query(sql,id)
        if user_profile:
            return user_profile[0]

    # 密码登录
    def pwdlogin(self,phone,auth_string):
        sql = "select * from users where u_phone=%s"
        user_profile = self.query(sql, phone)
        id, auth_str = (user_profile[0].get('id'),
                        user_profile[0].get('u_auth_string'))
        if check_password(auth_string, auth_str):
            return user_profile
        api_logger.warn('用户 %s 的口令不正确' % phone)
        return [{'code':'303','msg':'用户口令不正确'}]

    # 验证码登录
    def msglogin(self,u_phone,msg_code):
        res = check_sms(u_phone, msg_code)
        if not res:
            # 验证成功
            sql = 'select * from users where u_phone=%s'
            user_profile = self.query(sql, u_phone)
            if not bool(user_profile): # 手机未注册
                user_profile = self.msgregist(u_phone) # 注册
                return user_profile  # 返回用户信息，字典格式
            return user_profile[0]
        return res

    # 验证码注册
    def msgregist(self,u_phone):
        now_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        user_data = {'u_phone': u_phone, 'u_pname': 'EDU' + u_phone,
                     'u_create_time': now_time, 'is_active': 1, 'is_delete': 0}
        if self.save(**user_data): # 注册成功，返回用户信息
            user_profile = self.user_list('u_phone',u_phone)
            return user_profile[0]
        return {'code': 300, 'msg': '插入数据失败, 可能存在某一些字段没有给定值'}


if __name__ == '__main__':
    u_dao = UserDao()