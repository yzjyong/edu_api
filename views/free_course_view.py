from flask import Blueprint, jsonify

from dao.free_course_dao import FreeCourseDao

free_blue = Blueprint("combat_blue", __name__)


@free_blue.route("/course/list/", methods=["GET", "POST"])
def free_course_view():
    dao = FreeCourseDao()
    data = dao.free_course_query()
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