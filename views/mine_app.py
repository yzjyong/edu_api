from flask import Blueprint, jsonify

from dao.mine_dao import MineDao

mine_blue = Blueprint("mine_blue", __name__)


@mine_blue.route("/mine/", methods=["GET"])
def mine_view():
    dao = MineDao()
    data = dao.mine_query()
    if data:
        return jsonify({
            'code': 200,
            'msg': 'ok',
            'data': data
        })
    return jsonify({
        'code': 201,
        'msg': '请求数据失败',
    })