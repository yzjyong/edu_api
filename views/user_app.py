import random
from flask import Blueprint, request,jsonify
from libs import r,cache_
from dao.phone_dao import PhoneDao
from dao.user_dao import UserDao
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
                login_user = udao.pwdlogin(u_phone,u_auth_string)[0]
                if login_user.get('id'):
                    token = cache_.new_token()
                    cache_.save_token(token,login_user.get('id'))
                    udao.user_update('is_active', 1, 'u_phone', u_phone)
                    return jsonify({'code': 200,'token': token,'user_data': login_user})
                return jsonify(login_user)
            except Exception as e:
                return jsonify({'code': 202,'msg':str(e)})
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
        login_user = udao.msglogin(u_phone, msg_code)
        if login_user.get('id'):   # 验证码正确
            token = cache_.new_token()
            cache_.save_token(token, login_user.get('id'))
            udao.user_update('is_active', 1, 'u_phone', u_phone)
            # PhoneDao().save(**{'phone': u_phone, 'code': msg_code, 'send_type': '登录'})
            return jsonify({'code': 200, 'token': token, 'user_data': login_user})
        return jsonify(login_user)
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
                udao.user_update('is_active',1, 'u_phone', u_phone)
                # PhoneDao().save(**{'phone': u_phone, 'code': msg_code, 'send_type': '找回密码'})
                return jsonify({'code': 200, 'token': token, 'user_data': login_user})
            return jsonify(login_user)
        else:   # 手机号码不存在，提示
            return jsonify({'code': 300, 'msg': '请填写注册手机号'})
    else:
        return jsonify({
            'code': 101,
            'msg': '请求参数u_phone,msg_code,u_auth_string必须存在'
        })

# 退出登录
@blue.route('/loginout/',methods=['GET'])
def loginout():
    api_logger.debug('user forget get action!')
    token = request.args.get('token')
    print(token)
    try:
        id = r.get(token).decode()
        print(r.get(token))
        r.delete(token)
        UserDao().user_update('is_active', 0, 'id', id)
        return jsonify({'code':200,'msg':'退出成功！'})
    except Exception as e:
        return jsonify({'code':202,'msg':str(e)})


if __name__ == '__main__':
    print(r.get('f48553a82cea428ca5a48660317bc2c2'))