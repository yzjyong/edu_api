from dao import BaseDao
from logger import api_logger


class FreeCourseDao(BaseDao):

    def type_list(self, table_name, *fileds,where=None,condition=None, args=None):
        if not where:
            sql = "select {} from {}".format(','.join(*fileds), table_name)
        else:
            sql = "select {} from {} where {}{}{}".format(','.join(*fileds), table_name,where,condition, args)
        return self.query(sql)

    # def course_type_list(self, first_table_name, second_table_name, *fileds,
    #          where=None, args=None, frist_table_arg, second_table_arg):
    #     if not where:
    #         sql = "select {} from {} join {} on {}={} ".format \
    #             (','.join(*fileds), first_table_name, second_table_name, frist_table_arg, second_table_arg)
    #     else:
    #         sql = "select {} from {} join {} on {}={} where {}={}".format \
    #             (','.join(*fileds), first_table_name, second_table_name, frist_table_arg, second_table_arg, where, args)
    #     return self.query(sql)

    def free_course_query(self):
        try:
            courses_type = self.type_list('courses_type', ('course_id', 'name'))
            print(courses_type)
            courses_type_id = self.type_list('courses_type', ('id',), where='course_id', condition='=', args=1001)  # 获取默认大类id
            courses_child_type = self.type_list('courses_child_type', ('course_child_id', 'name'), where='course_type_id',
                                                condition='=',args=courses_type_id[0]['id'])  # 查询小类信息
            print(courses_child_type)
            courses = self.list('courses', ('course_id', 'name', 'img_url', 'is_free' ,'degree', 'study_num'),
                                where='is_free', args=True)  # 查询大类对应课程
            print(courses)
        except Exception as e:
            raise Exception({'code': 201, 'msg': e})

        return {
            "courses_type": courses_type,
            "course_child_type": courses_child_type,
            "courses": courses,
            }

    def couses_type_query(self, type_id):
        # 点击大类，返回小类名称及课程信息
        if type_id.isdigit():
            type_id = int(type_id)
            try:
                # 查询小类
                type_sql = 'select courses_child_type.course_child_id, courses_child_type.name, courses_child_type.img_url ' \
                           'from courses_child_type join courses_type on courses_type.id=courses_child_type.course_type_id ' \
                           'where courses_type.course_id=%s' % type_id
                course_sql = 'select courses.course_id, courses.name, courses.img_url, courses.is_free ,courses.degree,courses.study_num' \
                             ' from courses join courses_type on courses.course_type_id=courses_type.id where courses_type.course_id=%s limit 0, 20' % type_id
                type_message = self.query(type_sql)
                course_message = self.query(course_sql)
            except Exception as e:
                raise Exception({'code': 201, 'msg': '没有查询到相关数据'})
            if not type_message:
                # 没有查到
                raise Exception({'code': 201, 'msg': '没有查询到相关数据'})
            else:
                # 返回小类
                return {
                    "type_message": type_message
                }

if __name__ == '__main__':
    FreeCourseDao().free_course_query()