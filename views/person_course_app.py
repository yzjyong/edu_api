from flask import Blueprint, request, jsonify
from dao.person_combat_dao import PersonCombatDao
from libs.cache_ import get_token_user_id

per_course_blue = Blueprint('percourse_blue',__name__)

@per_course_blue.route('/percourse/',methods=['GET'],strict_slashes=False)
def person_combat():    # 我的课程
    resp = request.args
    if resp:
        token = resp.get('token')
        id = get_token_user_id(token)
        if id:
            per_combat_info = PersonCombatDao().comquery(id,1)
            if per_combat_info:
                course_id = [i['course_id'] for i in per_combat_info]
                u_course = {i:PersonCombatDao().u_course(course_id[i]) for i in range(len(course_id))}
                return jsonify(u_course)
            return jsonify({'code':203,'msg':'该用户暂无课程'})
        return jsonify({'code':203,'msg':'用户尚未登录'})
    return jsonify({'code': 304, 'msg': '传入数据为空'})

if __name__ == '__main__':
    print()