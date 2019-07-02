from dao import BaseDao


class CombatCourseDao(BaseDao):
    def type_list(self, table_name, *fields, where=None, args=None):
        if not where:
            sql = "select {} from {}".format(','.join(*fields), table_name)
        else:
            sql = "select {} from {} where {}={}".format(','.join(*fields), table_name, where, args)
        print(sql)
        return self.query(sql)

    def course_list(self, table_name, *fields, where, args, how, arg, page=1, page_size=20):
        sql = "select {} from {} where {}={} and {}={} limit {}, {}" \
            .format(','.join(*fields), table_name, where, args, how, arg, (page - 1) * page_size, page_size)
        print(sql)
        return self.query(sql)

    def course_sort_list(self, table_name, *fields, where, args, how, arg, field, sort='desc',  page=1, page_size=20):
        sql = "select {} from {} where {}={} and {}={} order by {} {} limit {}, {}" \
            .format(','.join(*fields), table_name, where, args, how, arg, field, sort, (page - 1) * page_size, page_size)
        print(sql)
        return self.query(sql)

    def combat_course_query(self):
        # 返回默认大类类型、小类类型及大类对应课程
        main_banner_data = self.list('main_banner', ('id', 'image_url'), where='sequence', args='90', page=1,
                                     page_size=3)
        print("main_banner_data", main_banner_data)
        courses_type = self.list('courses_type', ('course_id', 'name'), page_size=9)
        print("courses_type", courses_type)
        # 获取收费课程各个大类对应的课程的数量
        courses_num_count = self.count('courses', ('courses_type.course_id',), arg='courses.name', alias='num',
                                       second_table_name='courses_type', b_con='courses.course_type_id',
                                       a_con='courses_type.id', b_arg='courses.is_free', a_arg='false',
                                       args='courses.course_type_id')
        print("courses_num_count", courses_num_count)

        courses = self.course_list('courses',
                                   ('course_id', 'name', 'img_url', 'is_free', 'degree', 'study_num', 'price'),
                                   where='is_free', args=False, how='is_free', arg=False)  # 查询大类对应课程
        print("courses", courses)

        return {
            "main_banner_data": main_banner_data,
            "courses_type": courses_type,
            "courses_num_count": courses_num_count,
            "courses": courses,
        }

    def combat_course_type_query(self, type_id):
        # 点击收费课程大类返回相应数据
        if type_id.isdigit():
            type_id = int(type_id)
            # 查大类是否存在
            courses_type = self.type_list('courses_type', ('id',), where='course_id', args=type_id)

            if not courses_type:
                return None
            else:
                # 查询小类
                type_message = self.type_list('courses_child_type', ('course_child_id', 'name'),
                                              where='course_type_id', args=courses_type[0]['id'])
                # 查询对应课程
                courses_message = self.course_list('courses',
                                                   ('course_id', 'name', 'img_url', 'is_free', 'degree', 'study_num',
                                                    'price'),
                                                   where='course_type_id', args=courses_type[0]['id'], how='is_free',
                                                   arg=False)

                # 返回对应小类及对应课程
                return {
                    "type_message": type_message,
                    "courses_message": courses_message
                }

    def course_list_query(self, page):
        # ajax请求
        if page.isdigit():
            page = int(page)
            courses = self.list('courses',
                                ('course_id', 'name', 'img_url', 'is_free', 'degree', 'study_num', 'price'),
                                where='is_free', args=False, page=page)  # 查询大类对应课程
            print("courses", courses)
            if courses:
                return {
                    "courses": courses
                }
            else:
                return {
                    "courses": "没有更多课程了"
                }
        else:
            return None

    def course_api_query(self, type_id, sort, page):
        # ajax请求
        if type_id.isdigit():
            if page.isdigit():
                type_id = int(type_id)
                page = int(page)
                courses_type = self.type_list('courses_type', ('id',), where='course_id', args=type_id)
                if not courses_type:
                    type_message = self.type_list('courses_child_type', ('id',), where='course_child_id', args=type_id)
                    if not type_message:
                        return None
                    else:
                        courses_message = self.course_sort_list('courses',
                                                           ('course_id', 'name', 'img_url', 'is_free', 'degree',
                                                            'study_num', 'price'),
                                                           where='course_child_type_id', args=type_message[0]['id'],
                                                           how='is_free', arg=False, field=sort, page=page)
                        if not courses_message:
                            return "没有更多课程了"
                else:
                    courses_message = self.course_sort_list('courses',
                                                       ('course_id', 'name', 'img_url', 'is_free', 'degree',
                                                        'study_num', 'price'),
                                                       where='course_type_id', args=courses_type[0]['id'],
                                                       how='is_free', arg=False, field=sort, page=page)
                if not courses_message:
                    # 没查到相关数据
                    return "没有更多课程了"
                return {
                    "courses_message": courses_message
                }
        return None
# if __name__ == '__main__':
#     CombatCourseDao().course_list_query('2')
