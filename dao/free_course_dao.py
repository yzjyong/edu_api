from dao import BaseDao
from logger import api_logger


class FreeCourseDao(BaseDao):

    def type_list(self, table_name, *fileds,where=None,condition=None, args=None):
        if not where:
            sql = "select {} from {}".format(','.join(*fileds), table_name)
        else:
            sql = "select {} from {} where {}{}{}".format(','.join(*fileds), table_name,where,condition, args)
        print(sql)
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
        # 返回默认大类类型、小类类型及大类对应课程
        courses_type = self.type_list('courses_type', ('course_id', 'name'))
        print(courses_type)
        courses_type_id = self.type_list('courses_type', ('id',), where='course_id', condition='=', args=1001)  # 获取默认大类id
        courses_child_type = self.type_list('courses_child_type', ('course_child_id', 'name'), where='course_type_id',
                                            condition='=',args=courses_type_id[0]['id'])  # 查询小类信息
        print(courses_child_type)
        courses = self.list('courses', ('course_id', 'name', 'img_url', 'is_free', 'degree', 'study_num'),
                            where='is_free', args=True)  # 查询大类对应课程
        print(courses)


        return {
            "courses_type": courses_type,
            "course_child_type": courses_child_type,
            "courses": courses,
            }

    def couses_type_query(self, type_id):
        # 点击大类，返回小类名称及课程信息
        if type_id.isdigit():
            type_id = int(type_id)
            # 查大类是否存在
            courses_type = self.type_list('courses_type', ('id',), where='course_id',condition='=',  args=type_id)
            print(courses_type)
            if not courses_type:
                # 没有查到大类
                return None
            # 查询小类
            type_message = self.type_list('courses_child_type', ('course_child_id', 'name', 'img_url'),
                                                where='course_type_id', condition='=', args=courses_type[0]['id'])
            # 查询对应课程
            course_message = self.list('courses', ('course_id', 'name', 'img_url', 'is_free', 'degree', 'study_num'),
                                            where='course_type_id', args=courses_type[0]['id'])

            # 返回对应小类及对应课程
            return {
                "type_message": type_message,
                "course_message":course_message
            }

# if __name__ == '__main__':
#     FreeCourseDao().free_course_query()