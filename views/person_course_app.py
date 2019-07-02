from flask import Blueprint, request, jsonify
from dao.person_combat_dao import PersonCombatDao
from libs.cache_ import get_token_user_id,check_token

per_course_blue = Blueprint('percourse_blue',__name__)

@per_course_blue.route('/percourse/',methods=['GET'])
def person_course():    # 我的课程
    resp = eval(request.get_data())
    if resp:
        token = resp.get('token')
        if check_token(token):
            id = get_token_user_id(token)
            if id:
                per_combat_info = PersonCombatDao().comlist(('user_id','is_free'),(id,1))
                if per_combat_info:
                    course_id = per_combat_info[0]['course_id']
                    u_course = {i:PersonCombatDao().u_course(course_id[i]) for i in range(len(course_id))}
                    return jsonify(u_course)
                return jsonify({'code':203,'msg':'该用户暂无课程'})
            return jsonify({'code':203,'msg':'用户尚未登录'})
        return jsonify({'code': 304, 'msg': '传入数据不全'})
    return jsonify({'code': 304, 'msg': '传入数据为空'})