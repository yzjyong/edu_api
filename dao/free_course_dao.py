from dao import BaseDao


class FreeCourseDao(BaseDao):

    def free_course_query(self):
        try:
            sql1 = 'select course_id, name from courses_type '
            sql2 = 'select courses_child_type.course_child_id, courses_child_type.name, courses_type.course_id from ' \
                   'courses_child_type join courses_type on courses_child_type.course_type_id=courses_type.id '
            sql3 = 'select courses.course_id, courses.name, courses.img_url, courses.is_free ,courses.degree, ' \
                   'courses.study_num  from courses order by add_time desc limit 1, 20'
            courses_type = self.query(sql1)
            course_child_type = self.query(sql2)
            courses = self.query(sql3)
        except Exception as e:
            raise Exception({'code': 201, 'msg': e})

        return {
            "courses_type": courses_type,
            "course_child_type": course_child_type,
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
                             ' from courses join courses_type on courses.course_type_id=courses_type.id where courses_type.course_id=%s limit 1, 20' % type_id
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