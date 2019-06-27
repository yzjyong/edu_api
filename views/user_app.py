import random
from datetime import datetime
from flask import Blueprint, request,jsonify
from libs import r
from dao.phone_dao import PhoneDao
from dao.user_dao import UserDao
from libs import cache_
from libs.crypt import make_password
from logger import api_logger
from libs.sms import send_sms_code

blue = Blueprint("userblue",__name__)


# 发送短信验证码
@blue.route('/msgcode/',methods=['POST'])
def send_msg():
    u_phone = request.args.get('u_phone')
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    res = eval(send_sms_code(u_phone, code).decode())
    if res['Code'] == 'OK':
        try:
            r.setex('msg'+u_phone,code,120)  # 保存到redis缓存
        except Exception as e:
            api_logger.error(e)
            return jsonify({'code':802,'msg':'短信验证码保存失败'})
        api_logger.info('发送手机号：%s，短信验证码为：%s'%(u_phone,code))
        return jsonify({'code':200,'msg':'短信验证码发送成功！'})
    return jsonify({'code':303,'msg':'请输入正确的手机号码'})

# 检查手机号码
@blue.route('/checkphone/',methods=['GET'])
def check_phone():
    u_phone = request.args.get('u_phone')
    result = {
        'code': 200,
        'msg': '手机号不存在'
    }
    if UserDao().check_login_phone(u_phone):
        result['code'] = 205
        result['msg'] = '手机号已存在'

    return jsonify(result)

# 密码登录
@blue.route('/pwdlogin/',methods=['POST'])
def msglogin():
    api_logger.debug('user phone_login get action!')
    resp = eval(request.get_data().decode())
    u_phone = resp.get('u_phone')
    u_auth_string = resp.get('u_auth_string')
    if all((bool(u_phone),bool(u_auth_string))):
        udao = UserDao()
        # 验证手机号在数据库中是否存在
        if udao.check_login_phone(u_phone):
            try:
                # 验证密码是否正确
                login_user = udao.pwdlogin(u_phone,u_auth_string)
                if login_user.get('id'):
                    token = cache_.new_token()
                    cache_.save_token(token,login_user.get('id'))
                    udao.user_update('is_active', True, 'u_phone', u_phone)
                    udao.user_update('is_delete', True, 'False', u_phone)
                    return jsonify({'code': 200,'token': token,'user_data': login_user})
                else:
                    return jsonify(login_user)
            except Exception as e:
                return jsonify({'code': 202,'msg': e})
        return jsonify({'code': 304,'msg':'该手机尚未注册'})
    else:
        return jsonify({
            'code': 101,
            'msg': '请求参数u_phone和u_auth_string必须存在'
        })

# 验证码登录
@blue.route('/msglogin/',methods=['POST'])
def msg_login():
    api_logger.debug('user phone_login get action!')
    resp = eval(request.get_data().decode())
    u_phone = resp.get('u_phone')
    msg_code = resp.get('msg_code')
    if all((bool(u_phone),bool(msg_code))):
        udao = UserDao()
        if udao.check_login_phone(u_phone):
            login_user = udao.msglogin(u_phone,msg_code)
            if login_user.get('id'):
                token = cache_.new_token()
                cache_.save_token(token, id)
                udao.user_update('is_active', True, 'u_phone', u_phone)
                udao.user_update('is_delete', True, 'False', u_phone)
                # PhoneDao().save(**{'phone': u_phone, 'code': msg_code, 'send_type': '登录'})
                return jsonify({'code': 200,'token': token,'user_data': login_user})
            return jsonify(login_user)
        else:   # 如果用户名手机号码不存在，则直接新增用户
            now_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            user_data = {'u_phone': u_phone,'u_pname': 'EDU' + u_phone,
                         'u_create_time':now_time,'is_active':True,'is_delete':False}
            if udao.save(**user_data):
                # PhoneDao().save(**{'phone': u_phone, 'code': msg_code, 'send_type': '注册'})
                return jsonify({'code': 200, 'msg': 'ok'})
            else:
                return jsonify({'code': 300, 'msg': '插入数据失败, 可能存在某一些字段没有给定值'})
    else:
        return jsonify({
            'code': 101,
            'msg': '请求参数u_phone和msg_code必须存在'
        })

# 忘记密码
@blue.route('/forget/',methods=['POST'])
def forget_pwd():
    api_logger.debug('user forget get action!')
    resp = eval(request.get_data().decode())
    u_phone = resp.get('u_phone')
    msg_code = resp.get('msg_code')
    u_auth_string = resp.get('u_auth_string')
    if all((bool(u_phone), bool(msg_code),bool(u_auth_string))):
        udao = UserDao()
        # 验证手机号在数据库中是否存在
        if udao.check_login_phone(u_phone):
            login_user = udao.msglogin(u_phone, msg_code)
            if login_user.get('id'):
                token = cache_.new_token()
                cache_.save_token(token, id)
                udao.user_update('u_auth_string',u_auth_string, 'u_phone', u_phone)
                udao.user_update('is_active', True, 'u_phone', u_phone)
                udao.user_update('is_delete', True, 'False', u_phone)
                # PhoneDao().save(**{'phone': u_phone, 'code': msg_code, 'send_type': '找回密码'})
                return jsonify({'code': 200, 'token': token, 'user_data': login_user})
            return jsonify(login_user)
        else:   # 如果用户名手机号码不存在，提示
            return jsonify({'code': 300, 'msg': '请填写注册手机号'})
    else:
        return jsonify({
            'code': 101,
            'msg': '请求参数u_phone,msg_code,u_auth_string必须存在'
        })


if __name__ == '__main__':
    r.setex('msg' + '18729541662', '135525',3600)