from flask import Blueprint, request, jsonify

from libs.cache_ import get_token_user_id

blue = Blueprint('persblue',__name__)


@blue.route('/person/',methods=['GET'])
def personinfo():
    resp = request.get_data()
    if resp:
        token = resp.get('token')
        try:
            id = get_token_user_id(token)

        except Exception as e:
            return jsonify({'code': 202, 'msg': str(e)})
    return jsonify({'code': 304, 'msg': '传入数据为空'})