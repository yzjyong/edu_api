from flask import Blueprint, jsonify, request

from dao.free_course_dao import FreeCourseDao

combat_blue = Blueprint("combat_blue", __name__)


# @combat_blue.route("/course/combat/list/", methods=["GET"])
# def free_course_view():
#     dao = FreeCourseDao()
#     type_id = request.args.get("c", None)
#     if type_id is None:
#         data = dao.free_course_query()
#         if data:
#             return jsonify({
#                 'code': 200,
#                 'msg': 'ok',
#                 'data': data
#             })
#         return jsonify({
#             'code': 201,
#             'msg': '请求数据失败',
#         })
#     else:
#
#         data = dao.couses_type_query(type_id)
#         if data:
#             return jsonify({
#                 'code': 200,
#                 'msg': 'ok',
#                 'data': data
#             })
#         return jsonify({
#             'code': 201,
#             'msg': '请求数据失败',
#         })


# @combat_blue.route("/course/combat/listajax/", methods=["GET"])
# def ajax_course_view():
#     dao = FreeCourseDao()
#     type_id = request.args.get("c", '1001')
#     page = request.args.get("page", '1')
#     data = dao.ajax_course_query(type_id, page)
#     if data:
#         return jsonify({
#             'code': 200,
#             'msg': 'ok',
#             'data': data
#         })
#     return jsonify({
#         'code': 201,
#         'msg': '请求数据失败',
#     })
