from dao import BaseDao
from logger import api_logger


class FreeCourseDao(BaseDao):

    def type_list(self, table_name, *fileds, where=None, args=None):
        if not where:
            sql = "select {} from {}".format(','.join(*fileds), table_name)
        else:
            sql = "select {} from {} where {}={}".format(','.join(*fileds), table_name, where, args)
        print(sql)
        return self.query(sql)

    def course_list(self, table_name, *fileds, where, args, how, arg, page=1, page_size=20):
        sql = "select {} from {} where {}={} and {}={} limit {}, {}" \
            .format(','.join(*fileds), table_name, where, args, how, arg, (page - 1) * page_size, page_size)
        print(sql)
        return self.query(sql)

    def free_course_query(self):
        # 返回默认大类类型、小类类型及大类对应课程
        courses_type = self.type_list('courses_type', ('course_id', 'name'))
        print(courses_type)
        courses_type_id = self.type_list('courses_type', ('id',), where='course_id', args=1001)  # 获取默认大类id
        courses_child_type = self.type_list('courses_child_type',
                                            ('course_child_id', 'name', 'img_url'),
                                            where='course_type_id', args=courses_type_id[0]['id'])  # 查询小类信息
        print(courses_child_type)
        courses = self.course_list('courses',
                                   ('course_id', 'name', 'img_url', 'is_free', 'degree', 'study_num'),
                                   where='is_free', args=True, how='is_free', arg=True)  # 查询大类对应课程
        print(courses)

        return {
            "courses_type": courses_type,
            "courses_child_type": courses_child_type,
            "courses": courses,
        }

    def couses_type_query(self, type_id):
        # 点击大类，返回小类名称及课程信息
        if type_id.isdigit():
            type_id = int(type_id)
            # 查大类是否存在
            courses_type = self.type_list('courses_type', ('id',), where='course_id', args=type_id)

            if not courses_type:
                # 没有查到大类
                type_message = self.type_list('courses_child_type', ('id',), where='course_child_id', args=type_id)

                if not type_message:
                    # 没有查到小类
                    return None
                else:
                    courses_message = self.course_list('courses',
                                                       ('course_id', 'name', 'img_url', 'is_free', 'degree',
                                                        'study_num'),
                                                       where='course_child_type_id', args=type_message[0]['id'],
                                                       how='is_free', arg=True)
                    return {
                        "courses_message": courses_message
                    }
            else:
                # 查询小类
                type_message = self.type_list('courses_child_type',
                                              ('course_child_id', 'name', 'img_url'),
                                              where='course_type_id', args=courses_type[0]['id'])
                # 查询对应课程
                courses_message = self.course_list('courses',
                                                   ('course_id', 'name', 'img_url', 'is_free', 'degree', 'study_num'),
                                                   where='course_type_id', args=courses_type[0]['id'],
                                                   how='is_free', arg=True)

                # 返回对应小类及对应课程
                return {
                    "type_message": type_message,
                    "courses_message": courses_message
                }

    def ajax_course_query(self, type_id, page):
        # ajax 请求
        if type_id.isdigit():
            if page.isdigit():
                type_id = int(type_id)
                page = int(page)
                courses_type = self.type_list('courses_type', ('id',), where='course_id', args=type_id)
                print("courses_type", courses_type)
                if not courses_type:
                    type_message = self.type_list('courses_child_type', ('id',), where='course_child_id', args=type_id)
                    print("type_message", type_message)
                    if not type_message:
                        return None
                    else:
                        courses_message = self.course_list('courses',
                                                           ('course_id', 'name', 'img_url', 'is_free', 'degree',
                                                            'study_num'),
                                                           where='course_child_type_id', args=type_message[0]['id'],
                                                           how='is_free', arg=True, page=page)
                        if not courses_message:
                            return "没有更多课程了"
                else:
                    courses_message = self.course_list('courses',
                                                       ('course_id', 'name', 'img_url', 'is_free', 'degree',
                                                        'study_num'),
                                                       where='course_type_id', args=courses_type[0]['id'],
                                                       how='is_free', arg=True, page=page)
                if not courses_message:
                    # 没查到相关数据
                    return "没有更多课程了"
                return {
                    "courses_message": courses_message
                }
        return None

# if __name__ == '__main__':
#     FreeCourseDao().ajax_course_query(1002, 2)
