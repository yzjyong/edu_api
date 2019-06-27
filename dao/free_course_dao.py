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
