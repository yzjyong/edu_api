import redis,json
from flask import jsonify
from apps import app
from libs import r
from logger import api_logger


def check_sms(u_phone,msg_code):
    try:
        r_msg_code = r.get('msg' + u_phone)
    except Exception as e:
        api_logger.error(e)
        # raise Exception('数据库查询失败')
        return jsonify({'code': 202, 'msg': '数据库查询失败'})
    if not r_msg_code:
        # raise Exception('短信验证码已过期')
        # return json.dumps({'code': 203, 'msg': '短信验证码已过期'})
        with app.app_context():
            return jsonify({'code': 203, 'msg': '短信验证码已过期'})
    if r_msg_code != msg_code:
        # raise Exception('短信验证码输入错误')
        return jsonify({'code': 204, 'msg': '短信验证码输入错误'})
    return True

if __name__ == '__main__':
    print(check_sms('18729541665','135525'))