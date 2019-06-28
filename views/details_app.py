from flask import Blueprint, request,jsonify
from dao.details_dao import DetailsDao

blue = Blueprint('detailblue',__name__)

# 详情页
@blue.route('/learn/',methods=['POST'])
def course_learn():
    course_id = eval(request.get_data())['course_id']
    if course_id.isdigit():
        dao = DetailsDao()
        topcourse = dao.get_top(course_id)
        if topcourse:
            topdata = {'topcourse':topcourse}
            precourse,t_info = dao.get_presentation(course_id)
            data = {'topdata':topdata,'precourse':precourse,'t_info':t_info}
            return jsonify(data)
        return jsonify({'code':202,'msg':'该课程不存在'})
    return jsonify({'code':202,'msg':'路由不合法'})