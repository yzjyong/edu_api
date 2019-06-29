from flask import Blueprint, request,jsonify
from dao.details_dao import DetailsDao

blue = Blueprint('detailblue',__name__)

# 介绍页
@blue.route('/learn/',methods=['GET'])
def course_learn():
    resp = request.get_data()
    course_id = eval(resp)['course_id'] if bool(resp) else ''
    if course_id.isdigit():
        courseinfo = DetailsDao().c_info(course_id)
        if courseinfo:
            data = DetailsDao().c_presentation(courseinfo[0])
            return jsonify(data)
        return jsonify({'code':202,'msg':'该课程不存在'})
    return jsonify({'code':202,'msg':'路由不合法'})

# 详情页
@blue.route('/learn/chapter/',methods=['GET'])
def course_chapter():
    resp = request.get_data()
    course_id = eval(resp)['course_id'] if bool(resp) else ''
    if course_id.isdigit():
        courseinfo = DetailsDao().c_info(course_id)
        if courseinfo:
            data = DetailsDao().c_lesson(courseinfo[0]['id'])
            return jsonify(data)
        return jsonify({'code': 202, 'msg': '该课程不存在'})
    return jsonify({'code': 202, 'msg': '路由不合法'})


if __name__ == '__main__':
    print(''.isdigit())