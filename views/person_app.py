from flask import Blueprint, request, jsonify

from dao.person_dao import PersonDao
from libs.cache_ import get_token_user_id

blue = Blueprint('persblue',__name__)


# 展示个人中心
@blue.route('/person/',methods=['GET'])
def personinfo():
    resp = request.get_data()
    if resp: # 验证请求数据
        token = resp.get('token')
        id = get_token_user_id(token)
        if id:
            perinfo = PersonDao().perlist(id)
            if perinfo:
                return jsonify(perinfo)
            return jsonify({'code': 203, 'msg': '查询失败！'})
        else:
            return jsonify({'code': 203, 'msg': '你还未登录！'})
    return jsonify({'code': 304, 'msg': '传入数据为空'})


@blue.route('/change/')
def changeinfo():
    resp = request.get_data()
    if resp:
        token = resp.pop('token')
        id = get_token_user_id(token)
        if id:
            for k,v in resp.items():
                PersonDao().perupdate(k,v,id)
            return ({'code':200,'msg':'ok!'})
        else:
            return jsonify({'code': 203, 'msg': '你还未登录！'})
    return jsonify({'code': 304, 'msg': '传入数据为空'})


if __name__ == '__main__':
    d = {'name':'tom','age':18,'sex':'nan'}
    locals().update(d)