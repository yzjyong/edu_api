from flask import Blueprint, jsonify, request

from dao.combat_course_dao import CombatCourseDao

combat_blue = Blueprint("combat_blue", __name__)


@combat_blue.route("/course/combat/list/", methods=["GET"])
def combat_course_view():
    dao = CombatCourseDao()
    type_id = request.args.get('c')
    if type_id is None:
        data = dao.combat_course_query()
    else:
        data = dao.combat_course_type_query(type_id)
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


@combat_blue.route("/course/combat/courselist/", methods=["GET"])
def ajax_course_view():
    dao = CombatCourseDao()
    page = request.args.get("page", '2')
    data = dao.course_list_query(page)
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
