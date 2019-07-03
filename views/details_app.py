from flask import Blueprint, request,jsonify
from dao.details_dao import DetailsDao

blue = Blueprint('detailblue',__name__)

# 免费介绍页
@blue.route('/learn/',methods=['GET'])
def course_learn():
    resp = request.args
    course_id = resp.get('course_id') if bool(resp) else ''
    if course_id.isdigit():
        courseinfo = DetailsDao().c_info(course_id)
        if courseinfo:
            data = DetailsDao().c_presentation(courseinfo[0])
            course_type_id = courseinfo[0]["course_type_id"]
            child_type_id = courseinfo[0]['course_child_type_id']
            data['type'],data['child_type'] = DetailsDao().c_type(course_type_id,child_type_id)
            return jsonify(data)
        return jsonify({'code':201,'msg':'该课程不存在'})
    return jsonify({'code':202,'msg':'路由不合法'})

# 免费详情页
@blue.route('/learn/chapter/',methods=['GET'])
def course_chapter():
    resp = request.args
    course_id = resp.get('course_id') if bool(resp) else ''
    if course_id.isdigit():
        courseinfo = DetailsDao().c_info(course_id)
        if courseinfo:
            print(courseinfo[0]['id'])
            data = DetailsDao().c_chapters(courseinfo[0]['id'])
            course_type_id = courseinfo[0]["course_type_id"]
            child_type_id = courseinfo[0]['course_child_type_id']
            data[0]['type'], data[0]['child_type'] = DetailsDao().c_type(course_type_id,child_type_id)
            return jsonify(data)
        return jsonify({'code': 201, 'msg': '该课程不存在'})
    return jsonify({'code': 202, 'msg': '路由不合法'})

# 付费详情页
@blue.route('/paylearn/',methods=['GET'])
def pay_learn():
    resp = request.args
    course_id = resp.get('course_id') if bool(resp) else ''
    if course_id.isdigit():
        courseinfo = DetailsDao().c_info(course_id)
        if courseinfo:
            data = DetailsDao().pay_detail(courseinfo[0])
            if data:
                return jsonify(data)
            return jsonify({'code': 201, 'msg': '查询失败'})
        return jsonify({'code': 202, 'msg': '该课程不存在'})
    return jsonify({'code': 203, 'msg': '路由不合法'})


if __name__ == '__main__':
    print(''.isdigit())