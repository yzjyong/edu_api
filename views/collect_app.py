from flask import Blueprint, request, jsonify
from libs import cache_
from dao.collect_dao import CollectDao
from logger import api_logger

collect_blue = Blueprint("collect_blue", __name__)


@collect_blue.route("/collect/", methods=["GET", ])
def collect_course():
    token = request.headers.get("token")
    type1 = request.args.get("type")
    c_id = request.args.get("cid")
    u_id = cache_.get_token_user_id(token)
    print(type1,type(type1),"00000")
    print(u_id,type(u_id))
    if u_id:
        try:
            if type1 == "0":  # 如果type==0,则添加收藏当前课程
                collect_success = CollectDao().save("user_favorites", **{"user_id": u_id, "course_id": c_id})
                if collect_success:
                    return jsonify({"code": 200, "msg": "已收藏至我的收藏"})
            elif type1 == "1":  # 如果type==1,则取消收藏当前课程
                collect_cancel = CollectDao().cancel_user_collect(u_id, c_id)
                if collect_cancel:
                    return jsonify({"code": 200, "msg": "已取消收藏"})
        except Exception as e:
            api_logger.error(e)
            return jsonify({"code":400})
    return jsonify({"code": 201, "msg": "用户还未登录或注册"})


@collect_blue.route("/my_collect/", methods=["GET"])
def my_collect():
    token = request.headers.get("token")
    u_id = cache_.get_token_user_id(token)
    if u_id:
        my_collect = CollectDao().get_my_collect(u_id)  # 获取当前用户的收藏课程
        if my_collect:
            return jsonify({"code": 200, "data": my_collect})
        return jsonify({"code": 201, "msg": "暂无收藏课程"})
    return jsonify({"code": 201, "msg": "用户还未登录或注册"})
