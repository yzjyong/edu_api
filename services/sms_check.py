import json
from flask import jsonify
from libs import r
from logger import api_logger


def check_sms(u_phone,msg_code):
    res = None
    try:
        r_msg_code = r.get('msg' + u_phone)
        print(r_msg_code,'----')
        if not r_msg_code:
            print('=====')
            return {'code': 203, 'msg': '短信验证码已过期'}
        r_msg_code = r_msg_code.decode()
        if r_msg_code != msg_code:
            return {'code': 204, 'msg': '短信验证码输入错误'}
    except Exception as e:
        api_logger.error(e)
        res = {'code': 202, 'msg': '数据库查询失败'}
    return res

if __name__ == '__main__':
    # print(check_sms('18729541665','135525'))
    print(None.decode())